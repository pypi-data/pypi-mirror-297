import sys
from logging import Logger

import rich_click as click

import api

sys.path.append('../cli')

import api.project_api
import cli.ui as ui
from config import Config

DEMO_CLIENT_ID = 17
DEMO_CLIENT_NAME = 'demo'
DEMO_CLIENT_USER = 'demo@ackee.xyz'
DEMO_PROJECT = '4NWbTFse'

@click.command("init")
@click.pass_context
def init(ctx):
    logger: Logger = ctx.obj.get('logger')
    config: Config = ctx.obj.get('config')

    api_key = ui.ask_with_help(
        title='Wake Arena API key', 
        desc='The API key is needed to authorize the demo version of the CLI', 
        enter='Enter the API key',
    )

    config.add_client(
        name=DEMO_CLIENT_NAME, 
        user=DEMO_CLIENT_USER, 
        client_id=DEMO_CLIENT_ID, 
        token=api_key
    )
    
    project = {}

    with ui.spinner('Checking the API key'):
        try:
            project_api = api.ProjectApi(logger, client_id=DEMO_CLIENT_ID, token=api_key)
        
            project = project_api.get_project(DEMO_PROJECT)
        
            if project.get('id') != DEMO_PROJECT:
                ui.error('Invalid API key')
                return
            
            config.set_active_client(DEMO_CLIENT_NAME)
            config.set_active_project(DEMO_PROJECT)
            config.write()
        
        except api.project_api.ProjectApiError:
            ui.error('The API key is invalid, please repeat the init step and input valid API key')
            return

    ui.success(
        title='Successfully initialized! 🎉',
        lines=[
            'Current project set to ' + ui.highlight(project.get('name')) + f' ({project.get('id')})',
            'Go to folder with your Contract code and use ' + ui.command('check') + ' command'
        ])
