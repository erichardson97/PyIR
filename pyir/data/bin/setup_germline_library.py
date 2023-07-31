#!/bin/python3

import os
import sys
from os import path
import argparse
import urllib.request
import subprocess
from subprocess import run
import shutil

SPECIES = [{
    'name': 'human',
    'imgt_name': 'Homo_sapiens',
    'ig': {
        'V': ['IGHV','IGKV', 'IGLV'],
        'J': ['IGHJ', 'IGKJ', 'IGLJ'],
        'D': ['IGHD'],
    },
    'tcr': {
        'V': ['TRAV', 'TRBV', 'TRGV', 'TRDV'],
        'J': ['TRAJ', 'TRBJ', 'TRGJ', 'TRDJ'],
        'D': ['TRBD','TRDD']
    }
}, {
    'name': 'shark',
    'imgt_name': 'Chondrichthyes',
    'ig': {
        'V': ['IGHV'],
        'J': ['IGHJ'],
        'D': ['IGHD'],
    },
    'tcr': {
    }
},
    {
    'name': 'pig',
    'imgt_name': 'Sus_scrofa',
    'ig': {
        'V': ['IGHV','IGKV','IGLV'],
        'J': ['IGHJ', 'IGKJ','IGLJ'],
        'D': ['IGHD'],
    },
    'tcr': {
        'V': ['TRBV'],
        'J': ['TRBJ'],
        'D': ['TRBD']
    }
},
    {
    'name': 'cow',
    'imgt_name': 'Bos_taurus',
    'ig': {
        'V': ['IGHV','IGKV','IGLV'],
        'J': ['IGHJ', 'IGKJ','IGLJ'],
        'D': ['IGHD'],
    },
    'tcr': {
        'V': ['TRBV','TRDV','TRAV'],
        'J': ['TRBJ','TRDJ','TRAJ'],
        'D': ['TRBD','TRDD','TRBD']
    }
},
    {
    'name': 'camel',
    'imgt_name': 'Camelus_dromedarius',
    'ig': {
        'V': ['IGKV'],
        'J': ['IGKJ'],
    },
    'tcr': {
        'V': ['TRBV','TRDV','TRAV','TRGV'],
        'J': ['TRBJ','TRGJ'],
        'D': ['TRBD']
    }
},
    {
    'name': 'mouse',
    'imgt_name': 'Mus_musculus',
    'ig': {
        'V': ['IGHV', 'IGKV', 'IGLV'],
        'J': ['IGHJ', 'IGKJ', 'IGLJ'],
        'D': ['IGHD'],
    },
    'tcr': {
        'V': ['TRAV', 'TRBV', 'TRDV', 'TRGV'],
        'J': ['TRAJ', 'TRBJ', 'TRDJ', 'TRGJ'],
        'D': ['TRBD', 'TRDD']
    }
}, {
    'name': 'chicken',
    'imgt_name': 'Gallus_gallus',
    'ig': {
        'V': ['IGHV', 'IGLV'],
        'J': ['IGHJ', 'IGLJ'],
        'D': ['IGHD'],
    },
    'tcr': {}
}, {
    'name': 'macaque',
    'imgt_name': 'Macaca_fascicularis',
    'ig': {
        'V': ['IGHV'],
        'J': ['IGHJ'],
        'D': ['IGHD'],
    },
    'tcr': {
        'V': ['TRBV'],
        'J': ['TRBJ'],
        'D': ['TRBD']
    }
},  {
    'name': 'rhesus',
    'imgt_name': 'Macaca_mulatta',
    'ig': {
        'V': ['IGHV', 'IGKV', 'IGLV'],
        'J': ['IGHJ', 'IGKJ', 'IGLJ'],
        'D': ['IGHD'],
    },
    'tcr': {
        'V': ['TRAV', 'TRBV', 'TRDV', 'TRGV'],
        'J': ['TRAJ', 'TRBJ', 'TRDJ', 'TRGJ'],
        'D': ['TRBD', 'TRDD']
    }
}, {
    'name': 'alpaca',
    'imgt_name': 'Vicugna_pacos',
    'ig': {
        'V': ['IGHV'],
        'J': ['IGHJ'],
        'D': ['IGHD'],
    },
    'tcr': {
    }
}, {
    'name': 'rabbit',
    'imgt_name': 'Oryctolagus_cuniculus',
    'ig': {
        'V': ['IGHV', 'IGKV', 'IGLV'],
        'J': ['IGHJ', 'IGKJ', 'IGLJ'],
        'D': ['IGHD'],
    },
    'tcr': {
        'V': ['TRAV', 'TRBV', 'TRDV', 'TRGV'],
        'J': ['TRAJ', 'TRBJ', 'TRDJ', 'TRGJ'],
        'D': ['TRBD', 'TRDD']
    }
}, {
    'name': 'rat',
    'imgt_name': 'Rattus_norvegicus',
    'ig': {
        'V': ['IGHV', 'IGKV', 'IGLV'],
        'J': ['IGHJ', 'IGKJ', 'IGLJ'],
        'D': ['IGHD'],
    },
    'tcr': {
        'V': [],
        'J': [],
        'D': []
    }
}, {
    'name': 'rhesus_monkey',
    'imgt_name': 'Macaca_mulatta',
    'ig': {
        'V': ['IGHV', 'IGKV', 'IGLV'],
        'J': ['IGHJ', 'IGKJ', 'IGLJ'],
        'D': ['IGHD'],
    },
    'tcr': {
        'V': ['TRAV', 'TRBV', 'TRDV', 'TRGV'],
        'J': ['TRAJ', 'TRBJ', 'TRDJ', 'TRGJ'],
        'D': ['TRBD', 'TRDD']
    }
}]

parser = argparse.ArgumentParser()
parser.add_argument('basedir')
parser.add_argument('outdir')
parser.add_argument('overwrite', default = "False")
args = parser.parse_args()
args.overwrite = eval(args.overwrite)


if 'linux' in sys.platform:
    platform = 'linux'
elif 'darwin' in sys.platform:
    platform = 'darwin'
else:
    raise ValueError('Unsupported system platform: ' + sys.platform + ". Run setup_germline_library.py on a Linux or "
                                                                       "OSX machine")
print('setup args:', args)

def get_local_data():
    try:
        os.makedirs(path.join(args.outdir, 'Ig', 'human'))
    except FileExistsError:
        pass
    ig_c_file = path.join(args.outdir, 'Ig', 'human', 'human_gl_C.fasta')
    ig_c_db = path.join(path.dirname(ig_c_file), path.basename(ig_c_file).split('.')[0])

    shutil.copy2(path.join(args.basedir,'crowelab_data','human_gl_C.fasta'), ig_c_file)
    result = run(
        [path.join(args.basedir, 'bin', 'makeblastdb_' + platform), '-dbtype', 'nucl', '-hash_index', '-parse_seqids',
         '-in', ig_c_file, '-out', ig_c_db, '-title', ig_c_db], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True)
    print(result.stdout)

    try:
        os.makedirs(path.join(args.outdir, 'TCR', 'human'))
    except FileExistsError:
        pass
    tcr_c_file = path.join(args.outdir, 'TCR', 'human', 'human_TCR_C.fasta')
    tcr_c_db = path.join(path.dirname(tcr_c_file), path.basename(tcr_c_file).split('.')[0])

    shutil.copy2(path.join(args.basedir, 'crowelab_data', 'human_TCR_C.fasta'), tcr_c_file)
    print('here')
    result = run(
        [path.join(args.basedir, 'bin', 'makeblastdb_' + platform), '-dbtype', 'nucl', '-hash_index', '-parse_seqids',
         '-in', tcr_c_file, '-out', tcr_c_db, '-title', tcr_c_db], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True)
    print(result.stdout)

    try:
        shutil.rmtree(path.join(args.outdir, 'prot'))
    except FileNotFoundError:
        pass
    shutil.copytree(path.join(args.basedir,'crowelab_data','prot'), path.join(args.outdir, 'prot'))

def get_imgt_data():
    print('Downloading IMGT data.')
    for species in SPECIES:
        for gene_locus in ['ig', 'tcr']:
            outdir_subfolder = 'Ig' if gene_locus == 'ig' else 'TCR'
            gene_file_ext = 'gl' if gene_locus == 'ig' else 'TCR'
            locus_url_ext = 'IG' if gene_locus == 'ig' else 'TR'

            try:
                os.makedirs(path.join(args.outdir, outdir_subfolder, species['name']))
            except FileExistsError:
                pass

            for gene in species[gene_locus]:
                seen = set()
                gene_file = path.join(args.outdir, outdir_subfolder, species['name'], species['name'] + '_' + gene_file_ext + '_' + gene + '.fasta')
                gene_db = path.join(path.dirname(gene_file), path.basename(gene_file).split('.')[0])
                if (not os.path.exists(gene_file)) | (args.overwrite):
                    print('Here:)')
                    with open(gene_file, 'w') as fasta_out:
                        for locus in species[gene_locus][gene]:
                            locus_url = 'http://www.imgt.org/download/V-QUEST/IMGT_V-QUEST_reference_directory/' + \
                                        species['imgt_name'] + '/' + locus_url_ext + '/' + locus + '.fasta'
                            
                            print('Downloading from:', locus_url)
                            write_out = False
                            for line in urllib.request.urlopen(locus_url):
                                line = line.decode('utf-8')
                                if line[0] == '>':
                                    ls = line.strip().split('|')
                                    if ls[1] in seen:
                                        write_out = False
                                        continue
                                    if species['imgt_name'].replace('_',' ') in ls[2]:
                                        fasta_out.write('>' + ls[1] + '\n')
                                        seen.add(ls[1])
                                        write_out = True
                                    else:
                                        write_out = False
                                elif write_out:
                                    fasta_out.write(line.replace('.',''))
                ## aas.
                result = run([path.join(args.basedir,'bin','makeblastdb_' + platform), '-dbtype', 'nucl', '-hash_index', '-parse_seqids',
                     '-in', gene_file, '-out', gene_db, '-title', gene_db], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
                gene_file = path.join(args.outdir, outdir_subfolder, species['name'], species['name'] + '_' + 'aa' + '_' + gene + '.fasta')
                gene_db = path.join(path.dirname(gene_file), path.basename(gene_file).split('.')[0])
                imgt_name = species['imgt_name'].replace('_','+')
                seen = set()
                if (not os.path.exists(gene_file)) | (args.overwrite):
                    with open(gene_file, 'w') as fasta_out:
                        for locus in species[gene_locus][gene]:
                            locus_url = f'http://www.imgt.org/IMGT_GENE-DB/GENElect?query=7.3+{locus}&species={imgt_name}'
                            write_out = False
                            lines = [p.decode('utf-8') for p in urllib.request.urlopen(locus_url)]
                            headers = [k for k,p in enumerate(lines) if p.startswith('>')]
                            end_index = [k for k,p in enumerate(lines) if p.startswith('\r')]
                            for header_idx in range(0, len(headers)):
                                idx = headers[header_idx]
                                header = lines[headers[header_idx]]
                                ls = header.strip().split('|')
                                if ls[1] in seen:
                                    write_out = False
                                    continue
                                if species['imgt_name'].replace('_', ' ') in ls[2]:
                                    fasta_out.write('>' + ls[1] + '\n')
                                    if header_idx+1 < len(headers):
                                        block = lines[headers[header_idx]+1:headers[header_idx+1]]
                                    else:
                                        end = min([(k, k-idx) for k in end_index if k-idx > 0], key = lambda x:x[1])[0]
                                        block = lines[headers[header_idx]+1:end]
                                    sequence = ''.join([p.strip('\n').replace('.','') for p in block])
                                    fasta_out.write(sequence+'\n')
                                    seen.add(ls[1])
                                          
                result = run([path.join(args.basedir,'bin','makeblastdb_' + platform), '-dbtype', 'prot', '-hash_index', '-parse_seqids',
                     '-in', gene_file, '-out', gene_db, '-title', gene_db], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)

                print(result.stdout)
                
                
                
                

get_local_data()
get_imgt_data()
