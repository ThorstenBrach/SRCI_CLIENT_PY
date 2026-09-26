from typing import Protocol

class IMessageLogger(Protocol):
    
    from RobotLibrary.Structures.Miscellaneous.AlarmMessage import AlarmMessage
    from RobotLibrary.IEC_Types import IEC_String

    """
    IEC-Interface IMessageLogger als Python-Protocol.
    """

    def AddMessageLog(self, MessageLog: "AlarmMessage") -> None:
        """
        Message to add to the log.
        """
        ...

    def AddSystemLog(self, SystemLog: "IEC_String") -> None:
        """
        System message to add to the log.
        STRING(RobotLibraryParameter.MESSAGE_TEXT_LEN)
        """
        ...