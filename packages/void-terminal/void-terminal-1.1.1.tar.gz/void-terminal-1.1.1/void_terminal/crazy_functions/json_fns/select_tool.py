from void_terminal.crazy_functions.json_fns.pydantic_io import GptJsonIO, JsonStringError

def structure_output(txt, prompt, err_msg, run_gpt_fn, pydantic_cls):
    gpt_json_io = GptJsonIO(pydantic_cls)
    analyze_res = run_gpt_fn(
        txt, 
        sys_prompt=prompt + gpt_json_io.format_instructions
    )
    try:
        friend = gpt_json_io.generate_output_auto_repair(analyze_res, run_gpt_fn)
    except JsonStringError as e:
        return None, err_msg

    err_msg = ""
    return friend, err_msg


def select_tool(prompt, run_gpt_fn, pydantic_cls):
    pydantic_cls_instance, err_msg = structure_output(
        txt=prompt,
        prompt="According to the prompt, Which tool function should be called for analysis\n\n",
        err_msg=f"Cannot understand the contact person",
        run_gpt_fn=run_gpt_fn,
        pydantic_cls=pydantic_cls
    )
    return pydantic_cls_instance, err_msg