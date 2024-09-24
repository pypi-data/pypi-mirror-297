from ..instruction_selection import *
from ..response_selection import *
from ..prompt_selection import *
from ..model_selection import *
from ..instruction_selection import *
from ..api_selection import *
from ...specializations import *
import asyncio
def get_raw_response_directory():
    return os.path.join(os.getcwd(),"response_data")
def get_latest_file(directory):
    files = glob.glob(f"{directory}/*")
    latest_file = max(files, key=os.path.getmtime)
    return latest_file
def get_last_created_response_file_path():
    raw_response_directory = get_raw_response_directory()
    return get_latest_file(raw_response_directory)
def read_previous_query():
    recent_file_path = get_last_created_response_file_path()
    return safe_read_from_json(recent_file_path)
def parse_previous_query():
    response_mgr = ResponseFileCollator()
    return self.ordered_data[0]
def get_db_query():
    file_path = get_last_created_response_file_path()
    return generate_query_from_recent_response(file_path)
def get_prompt_manager(prompt=None,
                       prompt_data=None,
                           request_data=[''],
                           instruction_data=None,
                           chunk_token_distribution_number=None,
                           completion_percentage=None,
                           instruction_mgr=None,
                           notation=None,
                           model_mgr=None,
                           chunk_number=None,
                           chunk_type=None,
                           model=None):
  prompt = prompt or ''
  prompt_data = prompt_data or []
  request_data = request_data or [prompt]
  instruction_data = instruction_data or []
  chunk_token_distribution_number = chunk_token_distribution_number or 0
  completion_percentage = completion_percentage or 40
  chunk_number=chunk_number or 0
  model_mgr = model_mgr or get_model_mgr(model=model)
  instruction_mgr = instruction_mgr or get_instruction_manager(bool_list = [],instructions={})
  chunk_type = chunk_type or "CODE"
  return PromptManager(prompt_data=[prompt],
                           request_data=[''],
                           instruction_data=[],
                           chunk_token_distribution_number=0,
                           completion_percentage=40,
                           instruction_mgr=instruction_mgr,
                           notation=None,
                           model_mgr=get_model_mgr(model=model),
                           chunk_number=chunk_number,
                           chunk_type=chunk_type)
class nogui_setup_module():
    def __init__(self,api_key=None,
                   env_path=None,
                   model=None,
                   prompt=None,
                   completion_percentage=None,
                   prompt_data=[],
                   tableName=None,
                   additional_instructions=None,
                   instruction_bools=None):
        self.api_key = api_key or None
        self.env_path = env_path or None
        self.model = model or ''
        self.prompt= prompt or ''
        self.completion_percentage = completion_percentage or 40
        self.prompt_data = make_list(prompt_data or [])
        self.tableName = tableName or None
        self.additional_instructions = additional_instructions or {}
        self.instruction_bools = instruction_bools or {}
        if self.tableName:
            self.prompt_data.append(get_instruction_from_tableName(tableName=self.tableName))
            self.instruction_bools['database_query']=True
        self.api_mgr = ApiManager(api_key=self.api_key,env_path=self.env_path)
        self.model_mgr = ModelManager(input_model_name = self.model)
        self.inst_mgr = InstructionManager(self.additional_instructions,self.instruction_bools)
        self.prompt_mgr = get_prompt_manager(prompt=self.prompt,prompt_data=self.prompt_data,instruction_mgr=self.inst_mgr,model_mgr=self.model_mgr,instruction_data=self.inst_mgr.instructions,completion_percentage = self.completion_percentage)
        self.resp_mgr = ResponseManager(prompt_mgr=self.prompt_mgr,api_mgr=self.api_mgr)
    def calculate_extra_tokens(self,prompt=None):
        self.extra_tokens = (self.model_mgr.selected_max_tokens*self.completion_percentage) - num_tokens_from_string(self.prompt_mgr.create_prompt())
        return self.extra_tokens
    async def async_make_query(self):
        response_mgr = ResponseManager(prompt_mgr=self.prompt_mgr,api_mgr=self.api_mgr)
        response = await response_mgr.initial_query()
        return get_updated_response_content(response)
    def make_query(self):
        return asyncio.run(self.async_make_query())

