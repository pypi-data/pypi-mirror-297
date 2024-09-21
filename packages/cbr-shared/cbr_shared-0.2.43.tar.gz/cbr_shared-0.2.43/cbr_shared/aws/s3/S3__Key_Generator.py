from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Misc import utc_now

S3_PATH__WHEN_BLOCK_SIZE   = 5

class S3__Key_Generator(Type_Safe):
    root_folder        : str  = None
    server_name        : str  = None
    use_when           : bool = True
    use_date           : bool = True
    use_hours          : bool = True
    use_minutes        : bool = True
    save_as_gz         : bool = False
    s3_path_block_size : int = S3_PATH__WHEN_BLOCK_SIZE

    def create_path_elements__from_when(self, when=None):
        path_elements = []
        if self.root_folder     : path_elements.append(self.root_folder )
        if self.server_name     : path_elements.append(self.server_name )
        if self.use_when        :
            if not when:
                when = self.path__for_date_time__now_utc()
            if when:                # for the cases when path__for_date_time__now_utc returns and empty value
                path_elements.append(when             )

        return path_elements

    def create_s3_key(self, path_elements, file_id):
        path_elements.append(file_id)
        s3_key = '/'.join(path_elements) + '.json'
        if self.save_as_gz:
            s3_key += ".gz"
        return s3_key

    def path__for_date_time__now_utc(self):
        return self.path__for_date_time(utc_now())

    def path__for_date_time(self, date_time):
        minute       = date_time.minute
        date_path    = date_time.strftime('%Y-%m-%d')                          # Format the date as YYYY-MM-DD
        hour_path    = date_time.strftime('%H')                                # Format the hour
        minute_block = self.calculate_minute_block(minute)
        path_components = []
        if self.use_date:
            path_components.append(date_path   )
        if self.use_hours:
            path_components.append(hour_path   )
        if self.use_minutes:
            path_components.append(minute_block)
        s3_path = '/'.join(path_components)
        return s3_path

    def calculate_minute_block(self, minute):
        block_size   = self.s3_path_block_size                                  # get the block size in minutes (configurable)
        minute_block = f"{(int(minute) // block_size) * block_size:02d}"        # Calculate the block using the configurable block size
        return minute_block