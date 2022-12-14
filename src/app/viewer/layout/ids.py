# A set of functions that create pattern-matching callbacks of the subcomponents
class Ids:

    # VtkFileInputAIO
    dropdown = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "dropdown",
        "aio_id": aio_id,
    }

    downloadinput = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "downloadinput",
        "aio_id": aio_id,
    }
    downloadmesh = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "downloadmesh",
        "aio_id": aio_id,
    }
    downloader = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "downloader",
        "aio_id": aio_id,
    }

    textinput = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "textinput",
        "aio_id": aio_id,
    }
    textupload = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "textupload",
        "aio_id": aio_id,
    }
    textjsonstore = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "textjsonstore",
        "aio_id": aio_id,
    }
    texttoast = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "texttoast",
        "aio_id": aio_id,
    }

    fileupload = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "fileupload",
        "aio_id": aio_id,
    }
    filejsonstore = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "filejsonstore",
        "aio_id": aio_id,
    }
    filetoast = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "filetoast",
        "aio_id": aio_id,
    }

    exampletoast = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "exampletoast",
        "aio_id": aio_id,
    }

    # Sidepanel stuff
    sidepanel = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "sidepanel",
        "aio_id": aio_id,
    }
    open = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "open",
        "aio_id": aio_id,
    }
    close = lambda aio_id: {
        "component": "VtkFileInputAIO",
        "subcomponent": "close",
        "aio_id": aio_id,
    }

    # VtkMeshViewerAIO
    vtk = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "vtk",
        "aio_id": aio_id,
    }
    vtkholder = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "vtkholder",
        "aio_id": aio_id,
    }
    submittoast = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "submittoast",
        "aio_id": aio_id,
    }
    monitortoast = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "monitortoast",
        "aio_id": aio_id,
    }
    getmeshtoast = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "getmeshtoast",
        "aio_id": aio_id,
    }
    loading = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "loading",
        "aio_id": aio_id,
    }
    jsonstore = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "jsonstore",
        "aio_id": aio_id,
    }
    interval = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "interval",
        "aio_id": aio_id,
    }
    jobstore = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "jobstore",
        "aio_id": aio_id,
    }
    jobstatus = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "jobstatus",
        "aio_id": aio_id,
    }
    jobcomplete = lambda aio_id: {
        "component": "VtkMeshViewerAIO",
        "subcomponent": "jobcomplete",
        "aio_id": aio_id,
    }
