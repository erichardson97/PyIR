import os
import subprocess 


imgt_url = "https://www.imgt.org/download/GENE-DB/IMGTGENEDB-ReferenceSequences.fasta-AA-WithoutGaps-F+ORF+inframeP"

def fasta_parser(fasta_file):
  output = {}
  lines = open(fasta_file, 'r').readlines()
  headers = [k for k,p in enumerate(lines) if p.startswith('>')]
  for m in range(0, len(headers)):
      header_index = headers[m]
      next_header = headers[m+1] if m +1 != len(headers) else 0
      output[lines[header_index].strip('\n')] = ''.join([p.strip('\n') for p in lines[header_index+1:next_header]]) if next_header != 0 else lines[header_index+1:]
  return output
  
def download_imgt():
  file="AA_all.fasta"
  subprocess.call("wget {imgt_url} -O {file} -q", shell = True)
  seqs = fasta_parser(file)
  os.remove(file)
  return seqs
  
def filter_write(seqs, imgt_directory):
  v_regions = dict((k, seqs[k]) for k in seqs if ('V-REGION' in k)&('IG' in k))
  species = set([p.split('|')[2] for p in v_regions])
  desired_species = ['Homo sapiens', 'Mus musculus', 'Rattus norvegicus', 'Oryctolagus cuniculus', 'Macaca mulatta']
  species_mapping = dict((z, '|'.join([p for p in species if z in p])) for z in desired_species)

  genes = dict((k, dict((p,v_regions[p]) for p in v_regions if re.search(species_mapping[k], p))) for k in species_mapping)
  counts = dict((k, dict((p, [z for z in genes[k] if p in z]) for p in set([m.split("|")[1] for m in genes[k]]))) for k in species_mapping)

  ##not doing anything with that dict atm but should check multiply defined alleles across dif mus musculus strains :( currently arbitrary which strain wins.
  genes = dict((k, dict((p.split('|')[1],v_regions[p]) for p in v_regions if re.search(species_mapping[k], p))) for k in species_mapping)
  
  common_names = {'Homo sapiens':'human','Macaca mulatta':'rhesus_monkey','Oryctolagus cuniculus':'rabbit','Mus musculus':'mouse','Rattus norvegicus':'rat'}
  for species in genes:
    fname = f'{common_names[species]}_aa_V.fasta'
    with open(os.path.join(imgt_directory, common_names[species], fname), 'w') as k:
      for p in genes[species]:
        k.write('>'+p+'\n'+genes[species][p]+'\n')
        
   
