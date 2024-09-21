from pollination_dsl.dag import Inputs, DAG, task, Outputs
from dataclasses import dataclass
from typing import Dict, List

# pollination plugins and recipes
from pollination.honeybee_radiance.grid import MergeFolderData
from pollination.honeybee_radiance_postprocess.grid import MergeFolderData as MergeFolderDataPostProcess

from pollination.ladybug_comfort.map import MapResultInfo
from pollination.path.copy import Copy

# input/output alias
from pollination.alias.inputs.model import hbjson_model_grid_room_input
from pollination.alias.inputs.ddy import ddy_input
from pollination.alias.inputs.simulation import additional_idf_input
from pollination.alias.inputs.comfort import air_speed_input, met_rate_input, \
    clo_value_input, pmv_comfort_par_input, solar_body_par_indoor_input
from pollination.alias.inputs.north import north_input
from pollination.alias.inputs.bool_options import write_set_map_input
from pollination.alias.inputs.runperiod import run_period_input
from pollination.alias.inputs.radiancepar import rad_par_annual_input
from pollination.alias.inputs.grid import min_sensor_count_input, cpu_count
from pollination.alias.outputs.comfort import tcp_output, hsp_output, csp_output, \
    thermal_condition_output, operative_or_set_output, pmv_output, env_conditions_output

from ._prepare_folder import PrepareFolder
from ._energy import EnergySimulation
from ._view_factor import SphericalViewFactorEntryPoint
from ._radiance import RadianceMappingEntryPoint
from ._dynamic import DynamicContributionEntryPoint
from ._dynshade import DynamicShadeContribEntryPoint
from ._comfort import ComfortMappingEntryPoint


@dataclass
class PmvComfortMapEntryPoint(DAG):
    """PMV comfort map entry point."""

    # inputs
    model = Inputs.file(
        description='A Honeybee model in HBJSON file format.',
        extensions=['json', 'hbjson'],
        alias=hbjson_model_grid_room_input
    )

    epw = Inputs.file(
        description='EPW weather file to be used for the comfort map simulation.',
        extensions=['epw']
    )

    ddy = Inputs.file(
        description='A DDY file with design days to be used for the initial '
        'sizing calculation.', extensions=['ddy'],
        alias=ddy_input
    )

    north = Inputs.float(
        default=0,
        description='A a number between -360 and 360 for the counterclockwise '
        'difference between the North and the positive Y-axis in degrees.',
        spec={'type': 'number', 'minimum': -360, 'maximum': 360},
        alias=north_input
    )

    run_period = Inputs.str(
        description='An AnalysisPeriod string to set the start and end dates of '
        'the simulation (eg. "6/21 to 9/21 between 0 and 23 @1"). If None, '
        'the simulation will be annual.', default='', alias=run_period_input
    )

    additional_idf = Inputs.file(
        description='An IDF file with text to be appended before simulation. This '
        'input can be used to include EnergyPlus objects that are not '
        'currently supported by honeybee.', extensions=['idf'],
        optional=True, alias=additional_idf_input
    )

    cpu_count = Inputs.int(
        default=50,
        description='The maximum number of CPUs for parallel execution. This will be '
        'used to determine the number of sensors run by each worker.',
        spec={'type': 'integer', 'minimum': 1},
        alias=cpu_count
    )

    min_sensor_count = Inputs.int(
        description='The minimum number of sensors in each sensor grid after '
        'redistributing the sensors based on cpu_count. This value takes '
        'precedence over the cpu_count and can be used to ensure that '
        'the parallelization does not result in generating unnecessarily small '
        'sensor grids. The default value is set to 1, which means that the '
        'cpu_count is always respected.', default=500,
        spec={'type': 'integer', 'minimum': 1},
        alias=min_sensor_count_input
    )

    write_set_map = Inputs.str(
        description='A switch to note whether the output temperature CSV should '
        'record Operative Temperature or Standard Effective Temperature (SET). '
        'SET is relatively intense to compute and so only recording Operative '
        'Temperature can greatly reduce run time, particularly when air speeds '
        'are low. However, SET accounts for all 6 PMV model inputs and so is a '
        'more representative "feels-like" temperature for the PMV model.',
        default='write-op-map', alias=write_set_map_input,
        spec={'type': 'string', 'enum': ['write-op-map', 'write-set-map']}
    )

    air_speed = Inputs.file(
        description='A CSV file containing a single number for air speed in m/s or '
        'several rows of air speeds that align with the length of the run period. This '
        'will be used for all indoor comfort evaluation.', extensions=['txt', 'csv'],
        optional=True, alias=air_speed_input
    )

    met_rate = Inputs.file(
        description='A CSV file containing a single number for metabolic rate in met '
        'or several rows of met values that align with the length of the run period.',
        extensions=['txt', 'csv'], optional=True, alias=met_rate_input
    )

    clo_value = Inputs.file(
        description='A CSV file containing a single number for clothing level in clo '
        'or several rows of clo values that align with the length of the run period.',
        extensions=['txt', 'csv'], optional=True, alias=clo_value_input
    )

    solarcal_parameters = Inputs.str(
        description='A SolarCalParameter string to customize the assumptions of '
        'the SolarCal model.', default='--posture seated --sharp 135 '
        '--absorptivity 0.7 --emissivity 0.95',
        alias=solar_body_par_indoor_input
    )

    comfort_parameters = Inputs.str(
        description='An PMVParameter string to customize the assumptions of '
        'the PMV comfort model.', default='--ppd-threshold 10',
        alias=pmv_comfort_par_input
    )

    radiance_parameters = Inputs.str(
        description='Radiance parameters for ray tracing.',
        default='-ab 2 -ad 5000 -lw 2e-05',
        alias=rad_par_annual_input
    )

    # tasks
    @task(template=PrepareFolder)
    def prepare_folder(
        self, model=model, epw=epw, north=north, run_period=run_period,
        cpu_count=cpu_count, min_sensor_count=min_sensor_count
    ) -> List[Dict]:
        return [
            {
                'from': PrepareFolder()._outputs.results,
                'to': 'results'
            },
            {
                'from': PrepareFolder()._outputs.initial_results,
                'to': 'initial_results'
            },
            {
                'from': PrepareFolder()._outputs.metrics,
                'to': 'metrics'
            },
            {
                'from': PrepareFolder()._outputs.sensor_grids
            },
            {
                'from': PrepareFolder()._outputs.sensor_grids_folder,
                'to': 'radiance/grid'
            },
            {
                'from': PrepareFolder()._outputs.shortwave_resources,
                'to': 'radiance/shortwave/resources'
            },
            {
                'from': PrepareFolder()._outputs.longwave_resources,
                'to': 'radiance/longwave/resources'
            },
            {
                'from': PrepareFolder()._outputs.dynamic_abtracted_octrees
            },
            {
                'from': PrepareFolder()._outputs.dynamic_shade_octrees
            }
        ]

    @task(template=EnergySimulation)
    def energy_simulation(
        self, model=model, epw=epw, ddy=ddy, north=north, run_period=run_period,
        additional_idf=additional_idf
    ) -> List[Dict]:
        return [
            {
                'from': EnergySimulation()._outputs.energy,
                'to': 'energy'
            }
        ]

    @task(
        template=SphericalViewFactorEntryPoint,
        needs=[prepare_folder],
        loop=prepare_folder._outputs.sensor_grids,
        sub_folder='radiance/view_factor/{{item.full_id}}',
        sub_paths={
            'octree_file_view_factor': 'scene.oct',
            'sensor_grid': '{{item.full_id}}.pts',
            'view_factor_modifiers': 'scene.mod'
        }
    )
    def run_spherical_view_factor_simulation(
        self,
        radiance_parameters=radiance_parameters,
        octree_file_view_factor=prepare_folder._outputs.longwave_resources,
        grid_name='{{item.full_id}}',
        sensor_grid=prepare_folder._outputs.sensor_grids_folder,
        view_factor_modifiers=prepare_folder._outputs.longwave_resources
    ) -> List[Dict]:
        pass

    @task(
        template=RadianceMappingEntryPoint,
        needs=[prepare_folder],
        loop=prepare_folder._outputs.sensor_grids,
        sub_folder='radiance',
        sub_paths={
            'octree_file_with_suns': 'scene_with_suns.oct',
            'octree_file': 'scene.oct',
            'sensor_grid': '{{item.full_id}}.pts',
            'sky_dome': 'sky.dome',
            'sky_matrix': 'sky.mtx',
            'sky_matrix_direct': 'sky_direct.mtx',
            'sun_modifiers': 'suns.mod'
        }
    )
    def run_radiance_simulation(
        self,
        radiance_parameters=radiance_parameters,
        model=model,
        octree_file_with_suns=prepare_folder._outputs.shortwave_resources,
        octree_file=prepare_folder._outputs.shortwave_resources,
        grid_name='{{item.full_id}}',
        sensor_grid=prepare_folder._outputs.sensor_grids_folder,
        sensor_count='{{item.count}}',
        sky_dome=prepare_folder._outputs.shortwave_resources,
        sky_matrix=prepare_folder._outputs.shortwave_resources,
        sky_matrix_direct=prepare_folder._outputs.shortwave_resources,
        sun_modifiers=prepare_folder._outputs.shortwave_resources
    ) -> List[Dict]:
        return [
            {
                'from': RadianceMappingEntryPoint()._outputs.enclosures,
                'to': 'radiance/enclosures'
            },
            {
                'from': RadianceMappingEntryPoint()._outputs.shortwave_results,
                'to': 'radiance/shortwave/results'
            },
            {
                'from': RadianceMappingEntryPoint()._outputs.shortwave_grids,
                'to': 'radiance/shortwave/grids'
            }
        ]

    @task(
        template=DynamicShadeContribEntryPoint,
        needs=[prepare_folder, run_radiance_simulation],
        loop=prepare_folder._outputs.dynamic_shade_octrees,
        sub_folder='radiance',
        sub_paths={
            'octree_file': 'dynamic_shades/{{item.default}}',
            'octree_file_with_suns': 'dynamic_shades/{{item.sun}}',
            'sky_dome': 'sky.dome',
            'sky_matrix': 'sky.mtx',
            'sky_matrix_direct': 'sky_direct.mtx',
            'sun_modifiers': 'suns.mod',
            'sun_up_hours': 'sun-up-hours.txt'
        }
    )
    def run_radiance_shade_contribution(
        self,
        radiance_parameters=radiance_parameters,
        octree_file=prepare_folder._outputs.shortwave_resources,
        octree_file_with_suns=prepare_folder._outputs.shortwave_resources,
        group_name='{{item.identifier}}',
        sensor_grid_folder='radiance/shortwave/grids',
        sensor_grids=prepare_folder._outputs.sensor_grids,
        sky_dome=prepare_folder._outputs.shortwave_resources,
        sky_matrix=prepare_folder._outputs.shortwave_resources,
        sky_matrix_direct=prepare_folder._outputs.shortwave_resources,
        sun_modifiers=prepare_folder._outputs.shortwave_resources,
        sun_up_hours=prepare_folder._outputs.shortwave_resources
    ) -> List[Dict]:
        pass

    @task(
        template=DynamicContributionEntryPoint,
        needs=[prepare_folder, energy_simulation, run_radiance_simulation],
        loop=prepare_folder._outputs.dynamic_abtracted_octrees,
        sub_folder='radiance',
        sub_paths={
            'result_sql': 'eplusout.sql',
            'octree_file_spec': 'dynamic_groups/{{item.identifier}}/{{item.spec}}',
            'octree_file_diff': 'dynamic_groups/{{item.identifier}}/{{item.diff}}',
            'octree_file_with_suns': 'dynamic_groups/{{item.identifier}}/{{item.sun}}',
            'sky_dome': 'sky.dome',
            'sky_matrix': 'sky.mtx',
            'sky_matrix_direct': 'sky_direct.mtx',
            'sun_modifiers': 'suns.mod',
            'sun_up_hours': 'sun-up-hours.txt'
        },
    )
    def run_radiance_dynamic_contribution(
        self,
        radiance_parameters=radiance_parameters,
        result_sql=energy_simulation._outputs.energy,
        octree_file_spec=prepare_folder._outputs.shortwave_resources,
        octree_file_diff=prepare_folder._outputs.shortwave_resources,
        octree_file_with_suns=prepare_folder._outputs.shortwave_resources,
        group_name='{{item.identifier}}',
        sensor_grid_folder='radiance/shortwave/grids',
        sensor_grids=prepare_folder._outputs.sensor_grids,
        sky_dome=prepare_folder._outputs.shortwave_resources,
        sky_matrix=prepare_folder._outputs.shortwave_resources,
        sky_matrix_direct=prepare_folder._outputs.shortwave_resources,
        sun_modifiers=prepare_folder._outputs.shortwave_resources,
        sun_up_hours=prepare_folder._outputs.shortwave_resources
    ) -> List[Dict]:
        pass

    @task(
        template=ComfortMappingEntryPoint,
        needs=[
            prepare_folder, energy_simulation, run_radiance_simulation,
            run_radiance_dynamic_contribution, run_radiance_shade_contribution,
            run_spherical_view_factor_simulation
        ],
        loop=prepare_folder._outputs.sensor_grids,
        sub_folder='initial_results',
        sub_paths={
            'result_sql': 'eplusout.sql',
            'enclosure_info': '{{item.full_id}}.json',
            'view_factors': '{{item.full_id}}.npy',
            'modifiers': 'scene.mod',
            'indirect_irradiance': '{{item.full_id}}.ill',
            'direct_irradiance': '{{item.full_id}}.ill',
            'ref_irradiance': '{{item.full_id}}.ill',
            'sun_up_hours': 'sun-up-hours.txt',
            'trans_schedules': 'trans_schedules.json',
            'occ_schedules': 'occupancy_schedules.json'
        }
    )
    def run_comfort_map(
        self,
        epw=epw,
        result_sql=energy_simulation._outputs.energy,
        grid_name='{{item.full_id}}',
        enclosure_info='radiance/enclosures',
        view_factors='radiance/longwave/view_factors',
        modifiers=prepare_folder._outputs.longwave_resources,
        indirect_irradiance='radiance/shortwave/results/indirect',
        direct_irradiance='radiance/shortwave/results/direct',
        ref_irradiance='radiance/shortwave/results/reflected',
        sun_up_hours=prepare_folder._outputs.shortwave_resources,
        contributions='radiance/shortwave/dynamic/final/{{item.full_id}}',
        transmittance_contribs='radiance/shortwave/shd_trans/final/{{item.full_id}}',
        trans_schedules=prepare_folder._outputs.shortwave_resources,
        occ_schedules=prepare_folder._outputs.metrics,
        run_period=run_period,
        air_speed=air_speed,
        met_rate=met_rate,
        clo_value=clo_value,
        solarcal_par=solarcal_parameters,
        comfort_parameters=comfort_parameters,
        write_set_map=write_set_map
    ) -> List[Dict]:
        return [
            {
                'from': ComfortMappingEntryPoint()._outputs.results_folder,
                'to': 'initial_results/results'
            },
            {
                'from': ComfortMappingEntryPoint()._outputs.conditions,
                'to': 'initial_results/conditions'
            },
            {
                'from': ComfortMappingEntryPoint()._outputs.metrics,
                'to': 'initial_results/metrics'
            }
        ]

    @task(template=MergeFolderDataPostProcess, needs=[run_comfort_map])
    def restructure_temperature_results(
        self, input_folder='initial_results/results/temperature', extension='csv'
    ):
        return [
            {
                'from': MergeFolderDataPostProcess()._outputs.output_folder,
                'to': 'results/temperature'
            }
        ]

    @task(template=MergeFolderDataPostProcess, needs=[run_comfort_map])
    def restructure_condition_results(
        self, input_folder='initial_results/results/condition', extension='csv'
    ):
        return [
            {
                'from': MergeFolderDataPostProcess()._outputs.output_folder,
                'to': 'results/condition'
            }
        ]

    @task(template=MergeFolderDataPostProcess, needs=[run_comfort_map])
    def restructure_condition_intensity_results(
        self, input_folder='initial_results/results/condition_intensity', extension='csv'
    ):
        return [
            {
                'from': MergeFolderDataPostProcess()._outputs.output_folder,
                'to': 'results/condition_intensity'
            }
        ]

    @task(template=MergeFolderData, needs=[run_comfort_map])
    def restructure_tcp_results(
        self, input_folder='initial_results/metrics/TCP', extension='csv'
    ):
        return [
            {
                'from': MergeFolderData()._outputs.output_folder,
                'to': 'metrics/TCP'
            }
        ]

    @task(template=MergeFolderData, needs=[run_comfort_map])
    def restructure_hsp_results(
        self, input_folder='initial_results/metrics/HSP', extension='csv'
    ):
        return [
            {
                'from': MergeFolderData()._outputs.output_folder,
                'to': 'metrics/HSP'
            }
        ]

    @task(template=MergeFolderData, needs=[run_comfort_map])
    def restructure_csp_results(
        self, input_folder='initial_results/metrics/CSP', extension='csv'
    ):
        return [
            {
                'from': MergeFolderData()._outputs.output_folder,
                'to': 'metrics/CSP'
            }
        ]

    @task(template=MapResultInfo)
    def create_result_info(
        self, comfort_model='pmv', run_period=run_period, qualifier=write_set_map
    ) -> List[Dict]:
        return [
            {
                'from': MapResultInfo()._outputs.temperature_info,
                'to': 'results/temperature/results_info.json'
            },
            {
                'from': MapResultInfo()._outputs.condition_info,
                'to': 'results/condition/results_info.json'
            },
            {
                'from': MapResultInfo()._outputs.condition_intensity_info,
                'to': 'results/condition_intensity/results_info.json'
            },
            {
                'from': MapResultInfo()._outputs.tcp_vis_metadata,
                'to': 'metrics/TCP/vis_metadata.json'
            },
            {
                'from': MapResultInfo()._outputs.hsp_vis_metadata,
                'to': 'metrics/HSP/vis_metadata.json'
            },
            {
                'from': MapResultInfo()._outputs.csp_vis_metadata,
                'to': 'metrics/CSP/vis_metadata.json'
            }
        ]

    @task(template=Copy, needs=[create_result_info])
    def copy_result_info(
        self, src=create_result_info._outputs.temperature_info
    ) -> List[Dict]:
        return [
            {
                'from': Copy()._outputs.dst,
                'to': 'initial_results/conditions/results_info.json'
            }
        ]

    # outputs
    environmental_conditions = Outputs.folder(
        source='initial_results/conditions',
        description='A folder containing the environmental conditions that were input '
        'to the thermal comfort model. This includes the MRT (C), air temperature (C), '
        'longwave MRT (C), shortwave MRT delta (dC) and relative humidity (%).',
        alias=env_conditions_output
    )

    temperature = Outputs.folder(
        source='results/temperature', description='A folder containing CSV maps of '
        'Operative Temperature for each sensor grid. Alternatively, if the '
        'write-set-map option is used, the CSV maps here will contain Standard '
        'Effective Temperature (SET). Values are in Celsius.',
        alias=operative_or_set_output
    )

    condition = Outputs.folder(
        source='results/condition', description='A folder containing CSV maps of '
        'comfort conditions for each sensor grid. -1 indicates unacceptably cold '
        'conditions. +1 indicates unacceptably hot conditions. 0 indicates neutral '
        '(comfortable) conditions.', alias=thermal_condition_output
    )

    pmv = Outputs.folder(
        source='results/condition_intensity', description='A folder containing CSV maps '
        'of the Predicted Mean Vote (PMV) for each sensor grid. This can be used '
        'to understand not just whether conditions are acceptable but how '
        'uncomfortably hot or cold they are.', alias=pmv_output
    )

    tcp = Outputs.folder(
        source='metrics/TCP', description='A folder containing CSV values for Thermal '
        'Comfort Percent (TCP). TCP is the percentage of occupied time where '
        'thermal conditions are acceptable/comfortable.', alias=tcp_output
    )

    hsp = Outputs.folder(
        source='metrics/HSP', description='A folder containing CSV values for Heat '
        'Sensation Percent (HSP). HSP is the percentage of occupied time where '
        'thermal conditions are hotter than what is considered acceptable/comfortable.',
        alias=hsp_output
    )

    csp = Outputs.folder(
        source='metrics/CSP', description='A folder containing CSV values for Cold '
        'Sensation Percent (CSP). CSP is the percentage of occupied time where '
        'thermal conditions are colder than what is considered acceptable/comfortable.',
        alias=csp_output
    )
