Look at this:
defs:
    pipes:
      ticket_classifier:
        use: HfLocalTextClassificationPipe
        token: "{{ OTAI_HUGGINGFACE_EHS_TOKEN }}"
        prompt: "{{ data.ticket.subject }} {{ data.ticket.body }}"

      classification_generic:
        steps:
          - steps:
              - id: classify
                model: "{{ config.model }}"
                {{ defs.pipes.ticket_classifier }}


What the use_def should do is pretty simple it should just load from the ticket_classifier and override their config with the own.

So the rendering of this should result in:
      - id: classification_generic
        steps:
          - steps:
              - id: classify
                model: "{{ config.model }}"
                use: HfLocalTextClassificationPipe
                token: "{{ OTAI_HUGGINGFACE_EHS_TOKEN }}"
                prompt: "{{ data.ticket.subject }} {{ data.ticket.body }}"

