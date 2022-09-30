
## PipEnv Usage

- `pipenv lock` - creates a 'Pipfile.lock' file that stores a working version of the dependencies
- `pipenv lock -r > requirements.txt` - does the same but with a 'requirements.txt' file
- `pipenv install --ignore-pipfile` - installs the locked dependencies

## Code Templates:

- #### main.py Path
```python
router = APIRouter(
    prefix='/',
    tags=['Category'],
    dependencies=[Depends(get_db)]
)


@router.get('/path/{param}',
    response_model=Type,
    summary="Short Description",
    dependencies=[Depends(dependency), ...]
)
def function(param: type, db: Session = Depends(get_db)):
    """
    Description
    """
    result = crud.get_result(db, param)
    if classes is None:
        raise HTTPException(
            status_code=404,
            detail='Message!'
        )
    
    return result
  ```
