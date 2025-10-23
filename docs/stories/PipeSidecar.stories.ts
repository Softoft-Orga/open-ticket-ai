import PipeSidecar from '../.vitepress/components/pipe/PipeSidecar.vue'
import type {Meta, StoryObj} from '@storybook/vue3'
import type {PipeSidecar as PipeSidecarType} from '../.vitepress/components/pipe/pipeSidecar.types'

const meta: Meta<typeof PipeSidecar> = {
    title: 'Components/PipeSidecar',
    component: PipeSidecar,
    tags: ['autodocs'],
}
export default meta

type Story = StoryObj<typeof meta>

const addNotePipeSidecar: PipeSidecarType = {
    _version: '1.0.x',
    _class: 'open_ticket_ai.base.ticket_system_pipes.AddNotePipe',
    _extends: 'open_ticket_ai.core.pipeline.ConfigurablePipe',
    _title: 'Add Note',
    _summary: 'Appends a note/article to a ticket in the connected system.',
    _category: 'ticket-system',
    _inputs: {
        placement: 'flat',
        alongside: ['id', 'use'],
        params: {
            ticket_system_id: 'Target ticket system ID from registry',
            ticket_id: 'Target ticket ID',
            note: 'Note body text or UnifiedNote object',
        },
    },
    _defaults: {
        'note.visibility': 'internal',
    },
    _output: {
        state_enum: ['ok', 'skipped', 'failed'],
        description: 'Pipe returns a state and optional payload.',
        payload_schema_ref: 'OpenTicketAI.Pipes.AddNote.Result',
        examples: {
            ok: {
                state: 'ok',
                payload: {
                    note_id: 12345,
                },
            },
            skipped: {
                state: 'skipped',
                payload: {
                    reason: 'empty_note',
                },
            },
            failed: {
                state: 'failed',
                error: 'ticket_not_found',
            },
        },
    },
    _errors: {
        fail: [
            {
                code: 'ticket_not_found',
                when: 'Ticket ID does not exist',
            },
            {
                code: 'backend_unauthorized',
                when: 'Adapter cannot authenticate',
            },
        ],
        break: [
            {
                code: 'config_invalid',
                when: 'Required config missing or invalid type',
            },
        ],
        continue: [
            {
                code: 'empty_note',
                when: 'Empty note body → pipe returns skipped',
            },
            {
                code: 'visibility_not_supported',
                when: 'Adapter ignores unsupported visibility → skipped',
            },
        ],
    },
    _engine_support: {
        on_failure: false,
        on_success: false,
    },
    _examples: {
        minimal: `- id: add_note
  use: open_ticket_ai.base.ticket_system_pipes.AddNotePipe
  ticket_system_id: "otobo_znuny"
  ticket_id: "{{ context.ticket.id }}"
  note: "Investigating"`,
        full: `- id: add_note_after_classification
  use: open_ticket_ai.base.ticket_system_pipes.AddNotePipe
  ticket_system_id: "otobo_znuny"
  ticket_id: "{{ context.last_created_ticket_id }}"
  note:
    body: |
      Root cause: database connection pool exhaustion
      Action: increase pool to 50; enable slow query log
    visibility: public`,
        large: `- id: add_note_conditional
  use: open_ticket_ai.base.ticket_system_pipes.AddNotePipe
  ticket_system_id: "otobo_znuny"
  ticket_id: "{{ context.ticket.id }}"
  note:
    body: >
      Auto-update: classified as {{ context.classification.queue }}
      priority={{ context.classification.priority }}
    visibility: internal`,
    },
}

const updateTicketPipeSidecar: PipeSidecarType = {
    _version: '1.0.x',
    _class: 'open_ticket_ai.base.ticket_system_pipes.UpdateTicketPipe',
    _extends: 'open_ticket_ai.core.pipeline.ConfigurablePipe',
    _title: 'Update Ticket',
    _summary: 'Updates an existing ticket in the connected system with new data.',
    _category: 'ticket-system',
    _inputs: {
        placement: 'flat',
        alongside: ['id', 'use'],
        params: {
            ticket_system_id: 'Target ticket system ID from registry',
            ticket_id: 'Target ticket ID',
            updated_ticket: 'Ticket data to update (UnifiedTicket object or dict)',
        },
    },
    _defaults: {},
    _output: {
        state_enum: ['ok', 'skipped', 'failed'],
        description: 'Pipe returns a state and optional payload.',
        payload_schema_ref: 'OpenTicketAI.Pipes.UpdateTicket.Result',
        examples: {
            ok: {
                state: 'ok',
                payload: {
                    ticket_id: 12345,
                    updated_fields: ['subject', 'priority'],
                },
            },
            skipped: {
                state: 'skipped',
                payload: {
                    reason: 'no_changes_needed',
                },
            },
            failed: {
                state: 'failed',
                error: 'ticket_not_found',
            },
        },
    },
    _errors: {
        fail: [
            {
                code: 'ticket_not_found',
                when: 'Ticket ID does not exist',
            },
            {
                code: 'backend_unauthorized',
                when: 'Adapter cannot authenticate',
            },
            {
                code: 'update_failed',
                when: 'Backend rejected the update operation',
            },
        ],
        break: [
            {
                code: 'config_invalid',
                when: 'Required config missing or invalid type',
            },
            {
                code: 'invalid_ticket_data',
                when: 'Updated ticket data is malformed',
            },
        ],
        continue: [
            {
                code: 'no_changes',
                when: 'No actual changes to apply → pipe returns skipped',
            },
        ],
    },
    _engine_support: {
        on_failure: false,
        on_success: false,
    },
    _examples: {
        minimal: `- id: update_ticket
  use: open_ticket_ai.base.ticket_system_pipes.UpdateTicketPipe
  ticket_system_id: "otobo_znuny"
  ticket_id: "{{ context.ticket.id }}"
  updated_ticket:
    subject: "Updated subject"`,
        full: `- id: update_ticket_priority
  use: open_ticket_ai.base.ticket_system_pipes.UpdateTicketPipe
  ticket_system_id: "otobo_znuny"
  ticket_id: "{{ context.ticket.id }}"
  updated_ticket:
    subject: "{{ context.updated_subject }}"
    priority: "high"
    queue: "L2_Support"`,
        large: `- id: update_ticket_classification
  use: open_ticket_ai.base.ticket_system_pipes.UpdateTicketPipe
  ticket_system_id: "otobo_znuny"
  ticket_id: "{{ context.ticket.id }}"
  updated_ticket:
    subject: "CLASSIFIED: {{ context.classification.category }}"
    priority: "{{ context.classification.priority }}"
    queue: "{{ context.classification.queue }}"
    custom_fields:
      classification_confidence: "{{ context.classification.confidence }}"
      auto_classified: true`,
    },
}

export const AddNotePipe: Story = {
    render: (args) => ({
        components: {PipeSidecar},
        setup() {
            return {args}
        },
        template: '<PipeSidecar v-bind="args" />',
    }),
    args: {
        sidecar: addNotePipeSidecar,
    },
}

export const UpdateTicketPipe: Story = {
    render: (args) => ({
        components: {PipeSidecar},
        setup() {
            return {args}
        },
        template: '<PipeSidecar v-bind="args" />',
    }),
    args: {
        sidecar: updateTicketPipeSidecar,
    },
}

export const WithActions: Story = {
    render: (args) => ({
        components: {PipeSidecar},
        setup() {
            return {args}
        },
        template: `
            <PipeSidecar v-bind="args">
                <template #actions>
                    <div class="flex gap-2">
                        <button class="px-4 py-2 bg-vp-brand text-white rounded hover:opacity-90 text-sm">
                            Run Pipe
                        </button>
                        <button class="px-4 py-2 border border-vp-border text-vp-text-1 rounded hover:bg-vp-bg text-sm">
                            View Docs
                        </button>
                    </div>
                </template>
            </PipeSidecar>
        `,
    }),
    args: {
        sidecar: addNotePipeSidecar,
    },
}
