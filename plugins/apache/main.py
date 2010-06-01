from ajenti.ui import *
from ajenti.com import implements
from ajenti.app.api import ICategoryProvider
from ajenti.app.helpers import *
from ajenti.utils import *

from backend import *


class Apache(CategoryPlugin):
    implements((ICategoryProvider, 50))

    text = 'Apache'
    description = 'Web server'
    icon = '/dl/apache/icon.png'
    platform = ['Debian', 'Ubuntu']
    
    def on_session_start(self):
        self._tab = 0
        self._editing_host = ''
        
    def get_ui(self):
        hdr = UI.HContainer(
               UI.Image(file='/dl/apache/bigicon.png'),
               UI.Spacer(width=10),
               UI.VContainer(
                   UI.Label(text='Apache web server', size=5),
                   UI.Label(text=('is running' if is_running() else 'is stopped'))
               )
            )
            
        
        th = UI.DataTable()
        hr = UI.DataTableRow(
                UI.DataTableCell(UI.Label(), width='20px'),
                UI.DataTableCell(UI.Label(text='Name'), width='200px'),
                UI.DataTableCell(UI.Label(text='Controls'), width='150px'),
                header=True
             )
        th.appendChild(hr)
        
        for h in list_hosts():
            if host_enabled(h):
                ctl = UI.LinkLabel(text='Disable', id='stophost/' + h)
            else: 
                ctl = UI.LinkLabel(text='Enable', id='starthost/' + h)
            r = UI.DataTableRow(
                    UI.Image(file=('/dl/apache/' + ('run.png' if host_enabled(h) else 'stop.png'))),
                    UI.Label(text=h),
                    UI.HContainer(
                        UI.LinkLabel(text='Edit', id='edithost/' + h),
                        ctl
                    )
                )
            th.appendChild(r)
            
        phosts = UI.VContainer(th)
        
        
        pmods = UI.VContainer()
        
        tc = UI.TabControl(active=self._tab)
        tc.add('Hosts', phosts)
        tc.add('Modules', pmods)

        p = UI.VContainer(
                hdr,
                UI.Spacer(height=20),
                tc
            )

        if self._editing_host != '':
            dlg = UI.DialogBox(
                      UI.TextInputArea(name='config', text=read_host_config(self._editing_host).replace('\n', '[br]'), width=800, height=500),
                      title="Edit host config", id="dlgEditHost", action="/handle/dialog/submit/dlgEditHost"
                  )
            p.appendChild(UI.vnode(dlg))

        return p

    @event('linklabel/click')
    def on_llclick(self, event, params, vars=None):
        if params[0] == 'stophost':
            disable_host(params[1])
        if params[0] == 'starthost':
            enable_host(params[1])
        if params[0] == 'edithost':
            self._editing_host = params[1]

    @event('dialog/submit')
    def on_submit(self, event, params, vars=None):
        if params[0] == 'dlgEditHost':
            if vars.getvalue('action', '') == 'OK':
                save_host_config(self._editing_host, vars.getvalue('config', ''))
            self._editing_host = '' 
    
        
class ApacheContent(ModuleContent):
    module = 'apache'
    path = __file__