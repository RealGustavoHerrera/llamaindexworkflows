from workflows import Context
from my_workflow import MyWorkflow
from workflow_locking import WorkflowLocking

async def main():

    w =  MyWorkflow()
    print("flow created")
    result = await w.run()
    print("we are done!")
    print(str(result))
    
    w =  WorkflowLocking()
    print("locking flow created")
    result = await w.run(count=3)
    print("we are done!")
    print(str(result))

    #############################################
    #  context managed outside of the workflow  #
    #############################################

    workflow = MyWorkflow()
    ctx = Context(workflow)
    print("workflow with external context created")

    # passing the context to the workflow
    handler = workflow.run(ctx=ctx)
    result = await handler
    print(f"result from first call: {result}")

    # Optional: save the ctx somewhere and restore
    ctx_dict = ctx.to_dict()
    print(f"context: {ctx_dict}")

    #recover (or build) a context from dict
    ctx = Context.from_dict(workflow, ctx_dict)

    # continue with next run
    handler = workflow.run(ctx=ctx)
    result = await handler    
    print(f"result from second call: {result}")


if __name__ == "__main__":
    import asyncio
    print("Testing context in workflows")
    asyncio.run(main())
    