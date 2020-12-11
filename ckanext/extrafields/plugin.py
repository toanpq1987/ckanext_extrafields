# encoding: utf-8

import ckan.plugins as p
import ckan.plugins.toolkit as tk


class ExampleIDatasetFormPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)


    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')

    # def create_package_schema(self):
    #     # let's grab the default schema in our plugin
    #     schema = super(ExampleIDatasetFormPlugin, self).create_package_schema()
    #     # our custom field
    #     schema.update({
    #         'cong_field1': [tk.get_validator('ignore_missing'),
    #                         tk.get_converter('convert_to_extras')]
    #     })
    #     return schema

    # def update_package_schema(self):
    #     schema = super(ExampleIDatasetFormPlugin, self).update_package_schema()
    #     # our custom field
    #     schema.update({
    #         'cong_field1': [tk.get_validator('ignore_missing'),
    #                         tk.get_converter('convert_to_extras')]
    #     })
    #     return schema



    def _modify_package_schema(self, schema):

        # Add our custom_test metadata field to the schema, this one will use
        # convert_to_extras instead of convert_to_tags.
        schema.update({
                'cong_field1': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_extras')]
                })
        # Add our custom_resource_text metadata field to the schema
        schema['resources'].update({
                'file_idl' : [ tk.get_validator('ignore_missing') ]
                })
        schema['resources'].update({
                'network_config' : [ tk.get_validator('ignore_missing') ]
            })
        return schema

    def create_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema


    def show_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).show_package_schema()
        schema.update({
            'cong_field1': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')]
        })

        schema['resources'].update({
                'file_idl' : [ tk.get_validator('ignore_missing') ]
            })

        schema['resources'].update({
                'network_config' : [ tk.get_validator('ignore_missing') ]
            })
        
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
