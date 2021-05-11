
from datetime import datetime

def context_processor():
	return {
      'now':datetime.utcnow()
	}
