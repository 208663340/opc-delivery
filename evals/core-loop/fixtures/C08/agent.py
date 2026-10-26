def execute(action, external, checkpoints):
    if checkpoints.done(action.id):
        return
    result = external.create(action.payload)
    checkpoints.complete(action.id, result)
