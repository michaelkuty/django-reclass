from django.utils.functional import cached_property
from django_reclass.api import MasterClient
from csb.backends import ProductBackend


class SaltBackendMixin(object):

    config_keys = {
        "salt_master_port": 5000,
        "salt_master_host": 'cfg01.domain.com',
        "service_template_name": 'leonardo-site',
        "service_reclass_path": 'srv/salt/reclass/classes/system/leonardo/server/app/{name}.yml',
    }

    @property
    def salt_master(self):
        '''returns inicialized salt master client'''
        return MasterClient(host=self.config.salt_master_host,
                            port=self.config.salt_master_port)

    @cached_property
    def reclass_template(self):
        # slugify get name from some parameters

        template = self.create_reclass_template(
            label=self.label,
            user=self.user,
            path=self.config.service_reclass_path,
            dbtemplate=self.get_service_template(
                self.config.service_template_name),
            attrs=self.attrs,
            sync=True
        )
        return template

    def create_reclass_template(self, label, dbtemplate, path='', attrs={},
                                sync=False, user=None):
        '''create heat template from given user attributes

        then you can call template.create_stack()

        returns HeatTemplate
        '''
        from django_reclass.models import ReclassTemplate

        template, create = ReclassTemplate.objects.get_or_create(
            label=label,
            user=user,
            path=path,
            template=dbtemplate,
            defaults={
                'context': attrs,
                'sync': sync
            }
        )

        return template


class SaltBackend(ProductBackend, SaltBackendMixin):

    '''Salt Backend'''

    config_keys = {
        "salt_master_port": 5000,
        "salt_master_host": 'cfg01.domain.com',
        "service_template_name": 'leonardo-site',
        "service_reclass_path": 'srv/salt/reclass/classes/system/leonardo/server/app/{name}.yml',
    }

    def create(self):

        # generate service meta from given attributes and push it to master
        self.reclass_template.push()

        # add service.class path to node in reclass
        self.reclass_template.add_class_to_node(
            name=self.config.node_name, push=True)

        # call highstate on node
        self.salt_master.update(self.config.node_name,
                                cmd="salt {clients} state.sls postgresql,leonardo,supervisor,nginx")
