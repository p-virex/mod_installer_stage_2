import os
import shutil
import zipfile

from common.common_utils import resource_path
from common.constants import DROP_XVM_FOLDER, g_MODS_CONFIG, VERSION_CLIENT
from common.path import PATH_TO_CACHE_WOT


class InstallScenario:
    def __init__(self, data):
        self.frame = data['frame']
        self.install_panel = data['install_panel']
        self.event_list = data['event_list']
        self.event_progress_list = data['event_list']
        self.pos_progress = len(self.event_list)
        self.run_scenario()

    def run_scenario(self):
        self.preparing_game()
        self.install_mods()

    def preparing_game(self):
        pre_panel = self.frame.panel_init_dict['preparing_client']
        if pre_panel.checkbox_del_mods_cache.GetValue():
            self.send_msg(self.install_panel.get_text('install_del_game_cache'))
            self.remove_folders(DROP_XVM_FOLDER)
            self.update_progress_bar('del_mods_cache')

        if pre_panel.checkbox_del_game_cache.GetValue():
            self.send_msg(self.install_panel.get_text('install_del_cache'))
            self.remove_folders(DROP_XVM_FOLDER)
            self.update_progress_bar('del_game_cache')

        if pre_panel.checkbox_backup.GetValue():
            self.send_msg(self.install_panel.get_text('create_backup'))
            self.update_progress_bar('backup')

    def install_mods(self):
        client_path = self.frame.panel_init_dict['search_game'].game_path.GetStringSelection()
        mods_panel = self.frame.panel_init_dict['select_mods']

        for name_mod in mods_panel.selected_mods_list:
            for name_group, mods_info in g_MODS_CONFIG.items():
                if name_mod not in g_MODS_CONFIG[name_group].keys():
                    continue
                full_path = os.path.join(client_path, 'mods', VERSION_CLIENT.lstrip('v.'))
                if not os.path.isdir(full_path):
                    self.send_msg(self.install_panel.get_text('dir_not_found') % full_path)
                    return
                mod_path = os.path.normpath(g_MODS_CONFIG[name_group][name_mod][1])
                zip_file = zipfile.ZipFile(resource_path(mod_path), 'r')
                zip_file.extractall(full_path)
                zip_file.close()
                self.send_msg(self.install_panel.get_text('success_install') % name_mod)
                self.update_progress_bar(name_mod)
        self.send_msg(self.install_panel.get_text('mods_installed') % client_path)
        self.install_panel.button_back.Enable()

    def send_msg(self, msg):
        self.install_panel.logging_window.AppendText(msg + '\n')

    def update_progress_bar(self, remove_event):
        self.event_progress_list.remove(remove_event)
        self.install_panel.progress_bar.SetValue(self.pos_progress - len(self.event_progress_list))

    @staticmethod
    def remove_folders(list_folders):
        for folder in list_folders:
            path_to_folder = os.path.join(PATH_TO_CACHE_WOT, folder)
            if not os.path.isdir(path_to_folder):
                continue
            shutil.rmtree(path_to_folder, ignore_errors=True)
