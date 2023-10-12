from .funcs import clean, cut_prompt, batch, concatenate, copy_path

def main(args):
    import sys
    if len(args) == 1: 
        from .execute import execute
        execute(args[0])
    else: 
        sys.stderr.write('Usage: parryutil <config_path> ...\n')
        sys.exit(1)

def main_cli():
    import sys
    main(sys.argv[1:])


__version__ = '0.0.2'