from .projectsetup import ProjectSetupPlugin

def classFactory(iface):
    return ProjectSetupPlugin(iface)
