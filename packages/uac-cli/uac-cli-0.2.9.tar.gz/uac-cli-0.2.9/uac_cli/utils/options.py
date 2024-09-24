import click

output_option = click.option('--output', '-o', type=click.File('w'))
output_option_binary = click.option('--output', '-o', type=click.File('wb', encoding='utf-16'))
select_option = click.option('--select', '-s', help="select which field to be returned. JSONPATH")
input_option = click.option('--input', '-i', type=click.File('r'))
input_option_binary = click.option('--input', '-i', type=click.File('rb', encoding='utf-16'))
ignore_ids = click.option("--ignore-ids/--no-ignore-ids", "-ig/-nig", is_flag=True, default=True, help="Ignore sysIDs in the payload")