from youtube_autonomous.segments.segment import Segment
from youtube_autonomous.segments.enums import ProjectStatus, ProjectField, SegmentStatus
from youtube_autonomous.database.database_handler import DatabaseHandler
from moviepy.editor import concatenate_videoclips
from bson.objectid import ObjectId
from typing import Union


class Project:
    """
    Class that represents a whole video Project, containing different
    segments that are used to build consecutively to end being a whole
    video that is this project video.
    """
    id: str = None
    """
    The stringified mongo ObjectId that identifies this project in the
    database.
    """
    status: ProjectStatus = None
    """
    The current project status that allows us to know if this project
    has started or not, or even if it has been finished.
    """
    segments: list[Segment] = None
    """
    The array that contains this project segments that are used to build
    the whole project video.
    """
    __do_use_setter: bool = True
    """
    Internal variable to know if we should use the custom property setters
    or just assign the value directly.

    _This parameter is not manually set by the user._
    """
    __database_handler: DatabaseHandler = None
    """
    Object to interact with the database and get and create projects.

    _This parameter is not manually set by the user._
    """

    def __init__(self, id: Union[str, ObjectId], status: ProjectStatus, segments: list[Segment]):
        self.id = id
        # We avoid updating database 'status' at this point
        self.__do_use_setter = False
        self.status = status
        self.__do_use_setter = True
        self.segments = segments

        self.__database_handler = DatabaseHandler()

    @property
    def unfinished_segments(self) -> list[Segment]:
        """
        Returns all this project segments that has not been built at
        all (they are unfinished).
        """
        return [segment for segment in self.segments if segment.status != SegmentStatus.FINISHED]
    
    @property
    def id(self):
        return self.id

    @id.setter
    def id(self, id: Union[ObjectId, str]):
        if not id:
            raise Exception('No "id" provided.')

        if not isinstance(id, (str, ObjectId)):
            raise Exception('The "id" parameter is not a string or an ObjectId.')
        
        if isinstance(id, ObjectId):
            id = str(id)

        self.id = id

    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, status: Union[ProjectStatus, str] = ProjectStatus.TO_START):
        """
        Updates the 'status' property and also updates it in the database.
        """
        if not status:
            raise Exception('No "status" provided.')
        
        if not isinstance(status, (ProjectStatus, str)):
            raise Exception('The "status" parameter provided is not a ProjectStatus nor a string.')
        
        if isinstance(status, str) and not ProjectStatus.is_valid(status):
            raise Exception('The "status" provided string is not a valid ProjectStatus enum value.')
            
        status = ProjectStatus(status)
        
        self.status = status.value
        if self.__do_use_setter:
            self.__database_handler.__update_project_field(self.id, ProjectField.STATUS, status.value)

    @property
    def segments(self):
        return self.segments

    @segments.setter
    def segments(self, segments: list[Segment]):
        """
        Updates the 'segments' property with the provided 'segments' parameter.
        This method will check that any of the provided segments are Segment
        objects.
        """
        if not segments:
            raise Exception('No "segments" provided.')
        
        if any(not isinstance(segment, Segment) for segment in segments):
            raise TypeError('Some of the given "segments" is not a Segment.')      

        self.segments = segments
        
    def build(self, output_filename: str):
        """
        This method will make that all the segments contained in this
        project are built. It will build the unfinished ones and them
        concatenate them in a final video that is stored locally as
        'output_filename'.
        """
        # I make, by now, 'output_filename' mandatory for this purpose
        if not output_filename:
            raise Exception('No "output_filename" provided.')

        self.status = ProjectStatus.IN_PROGRESS

        for segment in self.unfinished_segments:
            segment.build()

        unfinished_segments_len = len(self.unfinished_segments)
        if unfinished_segments_len > 0:
            raise Exception(f'There are {str(unfinished_segments_len)} segments that have not been completely built (unfinished).')
        
        # I put them together in a whole project clip
        concatenate_videoclips([segment.full_filename for segment in self.segments], output_filename)

        self.status = ProjectStatus.FINISHED
