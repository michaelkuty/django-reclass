
from __future__ import unicode_literals

import yaml
import glob
import os
from optparse import make_option

from dbtemplates.models import Template
from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand, NoArgsCommand
from django.utils.text import slugify
from django_reclass.models import Reclass, ReclassTemplate


class Command(BaseCommand):

    help = "Import all files under reclass/classes and reclass/nodes"

    missing_args_message = ("No name or path ")

    def add_arguments(self, parser):
        parser.add_argument('-n', '--name',
                            action='store', dest='name', default=None,
                            help="Name of imported reclass.")
        parser.add_argument('-p', '--path',
                            action='store', dest='path', default=None,
                            help="Path to reclass.")

    def handle(self, *args, **options):

        def get_paths(path=None, paths=[], stdout=None):
            '''recursively walk directories'''
            if os.path.isdir(path) and not os.path.islink(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.yml'):
                            if file not in paths:
                                paths.append(os.path.join(path, root, file))
                    stdout.write('{}'.format(len(paths)))
                    for dr in dirs:
                        new_dir = os.path.join(path, root, dr)
                        if not os.path.islink(new_dir):
                            stdout.write(
                                'Leaving {} and continue in {}'.format(root, dr))
                            get_paths(new_dir, paths, stdout)
                        else:
                            return

        name = options['name']
        path = options['path']

        nodes_uri = os.path.join(path, 'nodes')
        classes_uri = os.path.join(path, 'classes')

        class_paths = []
        node_paths = []
        get_paths(classes_uri, class_paths, stdout=self.stdout)
        get_paths(nodes_uri, node_paths, stdout=self.stdout)

        self.stdout.write(
            'Successfully collected {} paths for import.'.format(len(class_paths) + len(node_paths)))

        def get_reclass_path(node_path):
            '''returns system.linux.system.virtualbox'''
            return node_path.replace(
                path, '').replace(
                '/', '.').replace('.yml', '').replace(
                'classes', '').replace('nodes', '').replace(
                '_generated', '')[1:]

        reclass, created = Reclass.objects.get_or_create(name=slugify(name),
                                                         defaults={'verbose_name': name})

        for cls_path in class_paths:

            try:
                with open(cls_path) as yaml_file:
                    data = yaml.load(yaml_file)
                    kw = {'name': cls_path}
                    if data:
                        kw['content'] = data
                    template, created = Template.objects.get_or_create(**kw)
                    reclass_template, created = ReclassTemplate.objects.get_or_create(
                        label=get_reclass_path(cls_path), path=cls_path,
                        template=template)
                    reclass.classes.add(reclass_template)
            except Exception as e:
                self.stderr.write(
                    'Skip {} because {} was raised during importing'.format(cls_path, e))

        self.stdout.write(
            'Successfully processed {} classes'.format(len(class_paths)))

        for cls_path in node_paths:
            try:
                with open(cls_path) as yaml_file:
                    data = yaml.load(yaml_file)
                    kw = {'name': cls_path}
                    if data:
                        kw['content'] = data
                    template, created = Template.objects.get_or_create(**kw)
                    reclass_template, created = ReclassTemplate.objects.get_or_create(
                        label=get_reclass_path(cls_path), path=cls_path,
                        template=template)
                    reclass.nodes.add(reclass_template)
            except Exception as e:
                self.stderr.write(
                    'Skip {} because {} was raised during importing'.format(cls_path, e))

        self.stdout.write('Successfully imported {} nodes and {} classes'.format(
            len(node_paths), len(class_paths)))
