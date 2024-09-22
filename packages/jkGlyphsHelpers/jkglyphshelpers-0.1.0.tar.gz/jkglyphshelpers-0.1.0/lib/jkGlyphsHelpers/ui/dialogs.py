from vanilla.dialogs import askYesNo


def AskYesNoCancel(message, title="Glyphs", default=0, informativeText=""):
    """
    AskYesNoCancel Dialog

    message             the string
    title               a title of the window
    default             index number of which button should be default
                        (i.e. respond to return)
    informativeText     A string with secondary information
    """
    return askYesNo(
        messageText=message, informativeText=informativeText, alertStyle="informational"
    )
