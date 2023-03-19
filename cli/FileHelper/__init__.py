import os

template_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Templates')

def fmt_create(template_name, inputs):
    with open(os.path.join(template_folder, template_name + '.txt'), 'r') as template_file:
        template = template_file.read()
        formatted = template.format(*inputs)
        with open(template_name, 'w') as f:
            f.write(formatted)