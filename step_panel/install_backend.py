import os
import shutil
import zipfile

from common.common_utils import resource_path
from common.constants import DROP_XVM_FOLDER, VERSION_CLIENT, DROP_GAME_FOLDER, SET_IN_GAME_FOLDER, ONLY_INT_VERSION
from common.path import PATH_TO_CACHE_WOT, g_MODS_CONFIG


class InstallScenario:
    def __init__(self, data):
        self.client_path = ''
        self.frame = data['frame']
        self.install_panel = data['install_panel']
        self.event_list = data['event_list']
        self.event_progress_list = data['event_list']
        self.pos_progress = len(self.event_list)

    def run_scenario(self):
        self.preparing_game()
        self.install_mods()

    def preparing_game(self):
        pre_panel = self.frame.panel_init_dict['preparing_client']

        if pre_panel.checkbox_del_old_mods.GetValue():
            client_path = self.frame.panel_init_dict['search_game'].game_path.GetStringSelection()
            self.send_msg(self.install_panel.get_text('del_mods_install'))
            mod_folder = os.path.join(client_path, 'mods', ONLY_INT_VERSION)
            self.remove_folders(os.path.join(client_path, 'mods'), [ONLY_INT_VERSION])
            if not os.path.exists(mod_folder):
                os.mkdir(mod_folder)
            self.update_progress_bar('del_mods')

        if pre_panel.checkbox_del_mods_cache.GetValue():
            self.send_msg(self.install_panel.get_text('install_del_game_cache'))
            self.remove_folders(PATH_TO_CACHE_WOT, DROP_XVM_FOLDER)
            self.update_progress_bar('del_mods_cache')

        if pre_panel.checkbox_del_game_cache.GetValue():
            self.send_msg(self.install_panel.get_text('install_del_cache'))
            self.remove_folders(PATH_TO_CACHE_WOT, DROP_GAME_FOLDER)
            self.update_progress_bar('del_game_cache')

        if pre_panel.checkbox_backup.GetValue():
            self.send_msg(self.install_panel.get_text('del_mods_install'))
            self.create_backup()
            self.update_progress_bar('backup')

    def install_mods(self):
        self.client_path = self.frame.panel_init_dict['search_game'].game_path.GetStringSelection()
        mods_panel = self.frame.panel_init_dict['select_mods']
        full_path = os.path.join(self.client_path, 'mods', VERSION_CLIENT.lstrip('v.'))
        if not os.path.isdir(full_path):
            self.send_msg(self.install_panel.get_text('dir_not_found') % full_path)
            return

        for name_mod in mods_panel.selected_mods_list:
            if g_MODS_CONFIG.get(name_mod):
                mod_path = os.path.normpath(g_MODS_CONFIG[name_mod][1])
                self.unpack_mod(mod_path, name_mod)
                continue
            for name_group, mods_info in g_MODS_CONFIG.items():
                if not isinstance(g_MODS_CONFIG[name_group], dict) or name_mod not in g_MODS_CONFIG[name_group].keys():
                    continue

                mod_path = os.path.normpath(g_MODS_CONFIG[name_group][name_mod][1])
                self.unpack_mod(mod_path, name_mod)
        self.send_msg(self.install_panel.get_text('mods_installed') % self.client_path)
        self.install_panel.button_back.Enable()

    def unpack_mod(self, mod_path, name_mod):
        full_path = self.client_path if SET_IN_GAME_FOLDER else os.path.join(self.client_path, 'mods', ONLY_INT_VERSION)
        zip_file = zipfile.ZipFile(resource_path(mod_path), 'r')
        zip_file.extractall(full_path)
        zip_file.close()
        self.send_msg(self.install_panel.get_text('success_install') % name_mod)
        self.update_progress_bar(name_mod)

    def create_backup(self):
        client_path = self.frame.panel_init_dict['search_game'].game_path.GetStringSelection()
        mods_folder_path = os.path.join(client_path, 'mods', ONLY_INT_VERSION)

        backup_folder = client_path + os.sep + 'mods_backup'
        if not os.path.exists(backup_folder):
            os.mkdir(backup_folder)
        path_to_zip = os.path.join(backup_folder, 'backup_mods_{}.zip'.format(VERSION_CLIENT))
        zip_p = zipfile.ZipFile(path_to_zip, mode='w')
        for root, dirs, files in os.walk(mods_folder_path):
            for file in files:
                zip_p.write(os.path.join(root, file))
        zip_p.close()

    def send_msg(self, msg):
        self.install_panel.logging_window.AppendText(msg + '\n')

    def update_progress_bar(self, remove_event):
        self.event_progress_list.remove(remove_event)
        self.install_panel.progress_bar.SetValue(self.pos_progress - len(self.event_progress_list))

    @staticmethod
    def remove_folders(path, list_folders):
        for folder in list_folders:
            path_to_folder = os.path.join(path, folder)
            if not os.path.isdir(path_to_folder):
                continue
            shutil.rmtree(path_to_folder, ignore_errors=True)
