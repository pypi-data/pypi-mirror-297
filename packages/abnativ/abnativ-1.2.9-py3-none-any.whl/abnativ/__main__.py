"""
 Copyright 2023. Aubin Ramon and Pietro Sormanni. CC BY-NC-SA 4.0
"""

import argparse
import sys
from . import update
from . import scoring
from . import training
from . import vhh_humanisation
from . import vh_vl_humanisation

USAGE = """

%(prog)s <command> [options]

AbNatiV provides three commands:
    - update: updates the default AbNatiV models to the latest version or specifies a tag to checkout
    - train: train AbNatiV on a new input dataset of antibody sequences
    - score: use a trained AbNatiV model (default or custom) to score a set of input antibody sequences
    - hum_vhh: humanise a VHH sequence by combining AbNatiV VH and VHH assessments (dual-control strategy)
    - hum_vh_vl: humanise a pair of VH/VL Fv sequences by increasing AbNatiV VH- and VL- humanness

see also
%(prog)s <command> score -h
%(prog)s <command> train -h
%(prog)s <command> hum_vhh -h
%(prog)s <command> hum_vh_vl -h
for additional help

Copyright 2023. Aubin Ramon and Pietro Sormanni. CC BY-NC-SA 4.0
"""


def main():

    if len(sys.argv) == 1:
        empty_parser = argparse.ArgumentParser(
            description="VQ-VAE-based assessment of antibody and nanobody nativeness for engineering, selection, and computational design",
            usage=USAGE
        )
        empty_parser.print_help(sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="VQ-VAE-based assessment of antibody and nanobody nativeness for engineering, selection, and computational design",
    )

    subparser = parser.add_subparsers()

    # INIT
    update_parser = subparser.add_parser("update", description="Updates the default AbNatiV models to the latest version or specifies a tag to checkout",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    update_parser.add_argument('-t', '--tag', help='Tag to checkout in the AbNatiV models repository', type=str, default=None)

    update_parser.set_defaults(func=lambda args: update.init(args))

    # TRAINING
    train_parser = subparser.add_parser("train",
                                        description="Train AbNatiV on a new input dataset of antibody sequences",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    train_parser.add_argument('-tr', '--train_filepath', help='Filepath to fasta file .fa with sequences for training', type=str,
                        default='train_2M.fa')

    train_parser.add_argument('-va', '--val_filepath', help='Filepath to fasta file .fa with sequences for validation', type=str,
                        default='val_50k.fa')

    train_parser.add_argument('-hp', '--hparams', help='Filepath to the hyperparameter dictionary .yml', type=str,
                        default='hparams.yml')

    train_parser.add_argument('-mn', '--model_name', help='Name of the model to save checkpoints in', type=str,
                        default='abnativ_v2')

    train_parser.add_argument('-align', '--do_align', help='Do the alignment and the cleaning of the given sequences before training. \
                              This step can takes a lot of time if the number of sequences is huge.', action="store_true")
    
    train_parser.add_argument('-ncpu', '--ncpu', help='If ncpu>1 will parallelise the algnment process', default=1)

    train_parser.add_argument('-isVHH', '--is_VHH', help='Considers the VHH seed for the alignment/ \
                              It is more suitable when aligning nanobody sequences', action="store_true")

    train_parser.set_defaults(func=lambda args: training.run(args))

    # SCORING
    score_parser = subparser.add_parser("score", description="Use a trained AbNatiV model (default or custom) to score a set of input antibody sequences",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    score_parser.add_argument('-nat', '--nativeness_type', help='To load the AbNatiV default trained models type VH, VKappa, VLambda, or VHH, \
                              otherwise add directly the path to your own AbNatiV trained checkpoint .ckpt', type=str,
                                default='VH')

    score_parser.add_argument('-mean', '--mean_score_only', help='Generate only a file with a score per sequence. \
                              If not, generate a second file with a nativeness score per positin with a probability score \
                              for each aa at each position.', action="store_true")

    score_parser.add_argument('-i', '--input_filepath_or_seq', help='Filepath to the fasta file .fa to score or directly \
                              a single string sequence', type=str,
                              default='to_score.fa')

    score_parser.add_argument('-odir', '--output_directory', help='Filepath of the folder where all files are saved', type=str,
                              default='abnativ_scoring')

    score_parser.add_argument('-oid', '--output_id', help='Prefix of all the saved filenames (e.g., name sequence)', type=str,
                              default='antibody_vh')

    score_parser.add_argument('-align', '--do_align', help='Do the alignment and the cleaning of the given sequences before scoring. \
                              This step can takes a lot of time if the number of sequences is huge.', action="store_true")
    
    score_parser.add_argument('-ncpu', '--ncpu', help='If ncpu>1 will parallelise the algnment process', default=1)

    score_parser.add_argument('-isVHH', '--is_VHH', help='Considers the VHH seed for the alignment. \
                              It is more suitable when aligning nanobody sequences', action="store_true")
    
    score_parser.add_argument('-v', '--verbose', help='Print more details about every step.', action="store_true")

    score_parser.add_argument('-plot', '--is_plotting_profiles', help='Plot profile for every input sequence and save them in {output_directory}/{output_id}_profiles.', action="store_true")

    score_parser.set_defaults(func=lambda args: scoring.run(args))

    # VHH HUMANISATION
    hum_vhh_parser = subparser.add_parser("hum_vhh", description="Use AbNatiV to humanise nanobody sequences by combining AbNatiV VH and VHH assessments (dual-control stategy).",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    hum_vhh_parser.add_argument('-i', '--input_filepath_or_seq', help='Filepath to the fasta file .fa to score or directly \
                              a single string sequence', type=str,
                              default='to_score.fa')

    hum_vhh_parser.add_argument('-odir', '--output_directory', help='Filepath of the folder where all files are saved', type=str,
                              default='abnativ_humanisation_vhh')

    hum_vhh_parser.add_argument('-oid', '--output_id', help='Prefix of all the saved filenames (e.g., name sequence)', type=str,
                              default='nanobody_vhh')

    hum_vhh_parser.add_argument('-VHscore', '--threshold_abnativ_score', help='Bellow the AbNatiV VH threshold score, a position is considered as a liability',
                              type=float, default=0.98)

    hum_vhh_parser.add_argument('-rasa', '--threshold_rasa_score', help='Above this threshold, the residue is considered solvent exposed and is considered for mutation',
                              type=float, default=0.15)

    hum_vhh_parser.add_argument('-isExhaustive', '--is_Exhaustive', help='If True, runs the Exhaustive sampling strategy. If False, runs the enhanced sampling method', action="store_true")

    hum_vhh_parser.add_argument('-fmut', '--forbidden_mut', help='List of string residues to ban for mutation, i.e. C M', nargs='*',
                              type=str, default=['C','M'])

    hum_vhh_parser.add_argument('-VHHdecrease', '--perc_allowed_decrease_vhh', help='Maximun ΔVHH score decrease allowed for a mutation',
                              type=float, default=1.5e-2)

    hum_vhh_parser.add_argument('-a', '--a', help='Used for enhanced sampling method in multi-objective selection function: aΔVH+bΔVHH',
                              type=float, default=0.8)

    hum_vhh_parser.add_argument('-b', '--b', help='Used for enhanced sampling method in multi-objective selection function: aΔVH+bΔVHH',
                              type=float, default=0.2)

    hum_vhh_parser.add_argument('-pdb', '--pdb_file', help='Filepath to a pdb crystal structure of the nanobody of interest used to compute \
                                the solvent exposure. If the PDB is not very cleaned that might lead to some false results (which should be flagged by the \
                                program). If None, will predict the structure using NanoBuilder2', type=str,
                              default=None)

    hum_vhh_parser.add_argument('-ch', '--ch_id', help='PDB chain id of the nanobody of interest. If -pdb is None, it does not matter', type=str,
                              default='H')
    
    hum_vhh_parser.set_defaults(func=lambda args: vhh_humanisation.run(args))

    # VH_VL HUMANISATION
    hum_vh_vl_parser = subparser.add_parser("hum_vh_vl", description="Use AbNatiV to humanise a pair of VH/VL Fv sequences by increasing AbNatiV VH- and VL- humanness.",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    hum_vh_vl_parser.add_argument('-i_vh', '--input_seq_vh', help='A single VH string sequence', type=str)

    hum_vh_vl_parser.add_argument('-i_vl', '--input_seq_vl', help='A single VL string sequence', type=str)

    hum_vh_vl_parser.add_argument('-odir', '--output_directory', help='Filepath of the folder where all files are saved', type=str,
                              default='abnativ_humanisation_vh_vl')

    hum_vh_vl_parser.add_argument('-oid', '--output_id', help='Prefix of all the saved filenames (e.g., name sequence)', type=str,
                              default='antibody_vh_vl')

    hum_vh_vl_parser.add_argument('-VHscore', '--threshold_abnativ_score', help='Bellow the AbNatiV VH threshold score, a position is considered as a liability',
                              type=float, default=0.98)

    hum_vh_vl_parser.add_argument('-rasa', '--threshold_rasa_score', help='Above this threshold, the residue is considered solvent exposed and is considered for mutation',
                              type=float, default=0.15)

    hum_vh_vl_parser.add_argument('-isExhaustive', '--is_Exhaustive', help='If True, runs the Exhaustive sampling strategy. If False, runs the enhanced sampling method', action="store_true")

    hum_vh_vl_parser.add_argument('-fmut', '--forbidden_mut', help='List of string residues to ban for mutation, i.e. C M', nargs='*',
                              type=str, default=['C','M'])

    hum_vh_vl_parser.add_argument('-pdb', '--pdb_file', help='Filepath to a pdb crystal structure of the nanobody of interest used to compute \
                                the solvent exposure. If the PDB is not very cleaned that might lead to some false results (which should be flagged by the \
                                program). If None, will predict the paired structure using ABodyBuilder2', type=str,
                              default=None)

    hum_vh_vl_parser.add_argument('-ch_vh', '--ch_id_vh', help='PDB chain id of the heavy chain of interest. If -pdb is None, it does not matter', type=str,
                              default='H')

    hum_vh_vl_parser.add_argument('-ch_vl', '--ch_id_vl', help='PDB chain id of the light chain of interest. If -pdb is None, it does not matter', type=str,
                              default='L')
    
    hum_vh_vl_parser.set_defaults(func=lambda args: vh_vl_humanisation.run(args))

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
