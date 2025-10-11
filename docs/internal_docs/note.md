Improvements:

Use decorators for extra jinja 3 templates.

Improve typing. Each Pipe should have a PipeConfig class and
the config.yml should be validated and the input to the Pipes should be validated. Use allow extra(thats probably it)

Create an extra JinjaFieldType that has a template and then when its rendered turns into rendered value.
Or Having a TemplateRendering class.
RawType is always = RenderedType | str | None

And have the PipesConfig in a params dict.
Write extensive tests to test the config behaviour before writing all the logic for it.

Having Real branches:

````yaml
-   id: update_branch
    type: if_else
    condition: "{{ has_failed('update_ticket') and config.update_on_error }}"
    depends_on: [ "update_ticket" ]
    then:
        -   id: update_branch_success
    else:
        -   id: update_branch_failure


-   id: add_success_note
    depends_on: [ "update_branch_success" ]

-   id: add_failure_note
    depends_on: [ "update_branch_failure" ]



````




Idea Predefined Templates / Presets

````yaml

- id: test_example
  use: open_ticket_ai.complex_pipe_builder
  build_pipe: >
      {{
      from_template("ticket_classification")
      .with("fetch_ticket_by", { queue: { name: "Support" })
      .with("classify_ticket", { model: "gpt-4", prompt: "Classify the ticket" })
      .with("update_ticket", { status: "classified" })
      
      }}
````