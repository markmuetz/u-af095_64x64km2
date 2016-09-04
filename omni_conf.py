# Demonstration omni_conf.py file.
# Please replace all values.
from collections import OrderedDict as odict

settings = {
    'ignore_warnings': True,
}

computer_name = open('computer.txt').read().strip()
computers = {
    'rdf-comp': {
        'dirs': {
            'output': '/nerc/n02/n02/mmuetz/omni_output/u-af095_64x64km2/output',
        }
    }
}

expts = ['15s', '30s', '60s', 'no_graupel']
for comp in computers.values():
    for expt in expts:
	comp['dirs']['work_' + expt] = '/nerc/n02/n02/mmuetz/um10.5_runs/20day/u-af095_64x64km2_1km_{0}/work'.format(expt)
	comp['dirs']['results_' + expt] = '/nerc/n02/n02/mmuetz/omni_output/u-af095_64x64km2_{}/results'.format(expt)


batches = odict(('batch{}'.format(i), {'index': i}) for i in range(4))
groups = odict()
nodes = odict()

for expt in expts:
    groups['pp1_' + expt] = {
	    'type': 'init',
	    'base_dir': 'work_' + expt,
	    'batch': 'batch0',
	    'filename_glob': '2000??????????/atmos/atmos.???.pp1',
	    }

    groups['nc1_' + expt] = {
        'type': 'group_process',
        'from_group': 'pp1_' + expt,
        'base_dir': 'results_' + expt,
        'batch': 'batch1',
        'process': 'convert_pp_to_nc',
    }

    base_nodes = ['precip_ts', 'shf_ts', 'lhf_ts', 'precip_conv_ts']
    base_vars = ['precip', 'shf', 'lhf']

    groups['surf_timeseries_' + expt] = {
        'type': 'nodes_process',
        'base_dir': 'results_' + expt,
        'batch': 'batch2',
        'nodes': [bn + '_' + expt for bn in base_nodes],
    }

    groups['surf_ts_plots_' + expt] = {
        'type': 'nodes_process',
        'base_dir': 'output',
        'batch': 'batch3',
        'nodes': ['surf_ts_plots_' + expt],
    }

    for bn, bv in zip(base_nodes, base_vars):
	nodes[bn + '_' + expt] = {
	    'type': 'from_group',
	    'from_group': 'nc1_' + expt,
	    'variable': bv,
	    'process': 'domain_mean',
	}

    nodes['precip_conv_ts_' + expt] = {
        'type': 'from_nodes',
        'from_nodes': ['precip_ts_' + expt],
        'process': 'convert_mass_to_energy_flux',
    }
    nodes['surf_ts_plots_' + expt] = {
        'type': 'from_nodes',
        'from_nodes': ['precip_conv_ts_' + expt, 'shf_ts_' + expt, 'lhf_ts_' + expt],
        'process': 'plot_multi_timeseries',
    }

variables = {
    'precip': {
        'section': 4,
        'item': 203,
    },
    'shf': {
        'section': 3,
        'item': 217,
    },
    'lhf': {
        'section': 3,
        'item': 234,
    },
}
    
process_options = {
}
