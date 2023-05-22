<template lang="pug">
q-page(padding)

  // List
  section(v-if="view === 'list'")
    .q-pa-md
      c-table(icon="people" :title="$t('persona')" :rows="rows" :columns="columns" :loading="loading"
        @request="onRequest" @add="newPersona" @edit="editPersona" @view="viewPersona")

  // Edit
  section(v-if="view === 'new' || view === 'edit'")
    q-card
      q-card-section
        .text-h6 {{ view === 'edit' ? $t('general_edit') : $t('general_new') }} {{ $t('persona') }}
        .text-subtitle2 {{ $t('general_complete_the_data') }}
      q-separator

      q-card-section.flex.flex-center
        q-form(@submit='onSubmit' color='positive' :style="{'width': '60%'}")
          q-card(flat bordered)
            q-card-section

              .q-gutter-md
                .q-pa-md
                  .q-gutter-md.row
                    .col
                      c-input(v-model='persona.documento' :label="$t('persona_documento')" :hint="$t('page_field_hint', { entity: $t('persona_documento') })")

                      c-input(v-model='persona.nombre' :label="$t('persona_nombre')" :hint="$t('page_field_hint', { entity: $t('persona_nombre') })")

                      c-input(v-model='persona.apellido' :label="$t('persona_apellido')" :hint="$t('page_field_hint', { entity: $t('persona_apellido') })")

                      c-input(v-model='persona.ciudad' :label="$t('persona_ciudad')" :hint="$t('page_field_hint', { entity: $t('persona_ciudad') })")

                      c-input(v-model='persona.direccion' :label="$t('persona_direccion')" :hint="$t('page_field_hint', { entity: $t('persona_direccion') })")

                      c-input(v-model='persona.telefono' :label="$t('persona_telefono')" :hint="$t('page_field_hint', { entity: $t('persona_telefono') })")

                      c-input(v-model='persona.email' :label="$t('persona_email')" :hint="$t('page_field_hint', { entity: $t('persona_email') })")

            q-separator

            q-card-actions(align='around')
              q-btn(@click='cancelEdit' flat) {{ $t('general_back') }}
              q-btn(type='submit' flat color='positive' :loading='loading') {{ $t('general_save') }}
              q-space(v-if="view === 'edit'")
              q-btn(v-if="view === 'edit'" @click.prevent="onDelete" flat color="negative" :loading="loading")  {{ $t('general_delete') }}

  // Vista de visualización
  section(v-if="view === 'view'")
    q-card
      q-card-section
        .text-h6 {{ $t('general_view') }} {{ $t('persona') }}

        .q-pa-md
          .q-gutter-md.row
            .col

              .text-h6 {{ $t('persona_documento') }}
              p {{persona.documento}}

              .text-h6 {{ $t('persona_nombre') }}
              p {{persona.nombre}}

              .text-h6 {{ $t('persona_apellido') }}
              p {{persona.apellido}}

              .text-h6 {{ $t('persona_ciudad') }}
              p {{persona.ciudad}}

              .text-h6 {{ $t('persona_direccion') }}
              p {{persona.direccion}}

              .text-h6 {{ $t('persona_telefono') }}
              p {{persona.telefono}}

              .text-h6 {{ $t('persona_email') }}
              p {{persona.email}}

      q-separator

      q-card-actions(align="around")
        q-btn(@click="view = 'list'" flat) {{ $t('general_back') }}
        //q-btn(flat color="positive") $t('general_accept')

</template>

<script>
import { useQuasar } from 'quasar'
import { onMounted, ref, computed } from 'vue'
import { api } from 'boot/axios'
import { i18n } from 'boot/i18n.js'
import CTable from 'components/CTable.vue'
import CInput from 'components/CInput.vue'

const $t = i18n.global.t

const clearPersona = () => {
  return {
    id: null,
    documento: null,
    nombre: null,
    apellido: null,
    ciudad: null,
    direccion: null,
    telefono: null,
    email: null
  }
}

let instanceRef = null
let previousValues = {}

export default {
  name: 'PersonaPage',
  components: { CInput, CTable },

  setup() {
    const $q = useQuasar()

    const view = ref('list')
    const rows = ref([])
    const loading = ref(false)

    // Ref to mantain the pagination state when the c-table is removed from the dom (with v-if)
    const pagination = ref({
      sortBy: '',
      descending: true,
      page: 1,
      rowsPerPage: 10,
      rowsNumber: 0
    })
    const persona = ref(clearPersona())

    // for date values ==> field: row => date.formatDate(row.fecha_alta, 'YYYY-MM-DD'),
    // for transitive values ==> field: row => row.tipo_documento?.valor,

    const columns = computed(() => [
      {
        name: 'documento',
        label: $t('persona_documento'),
        align: 'left',
        field: 'documento',
        type: 'string',
        sortable: true
      },
      {
        name: 'nombre',
        label: $t('persona_nombre'),
        align: 'left',
        field: 'nombre',
        type: 'string',
        sortable: true
      },
      {
        name: 'apellido',
        label: $t('persona_apellido'),
        align: 'left',
        field: 'apellido',
        type: 'string',
        sortable: true
      },
      {
        name: 'ciudad',
        label: $t('persona_ciudad'),
        align: 'left',
        field: 'ciudad',
        type: 'string',
        sortable: true
      },
      {
        name: 'direccion',
        label: $t('persona_direccion'),
        align: 'left',
        field: 'direccion',
        type: 'string',
        sortable: true
      },
      {
        name: 'telefono',
        label: $t('persona_telefono'),
        align: 'left',
        field: 'telefono',
        type: 'string',
        sortable: true
      },
      {
        name: 'email',
        label: $t('persona_email'),
        align: 'left',
        field: 'email',
        type: 'string',
        sortable: true
      },
      {
        name: 'action',
        align: 'center',
        label: $t('general_actions'),
        field: 'action'
      }
    ])

    const newPersona = () => {
      persona.value = clearPersona()
      view.value = 'new'
    }

    const editPersona = async (instance) => {
      instanceRef = instance
      previousValues = { ...instance }
      persona.value = instance
      view.value = 'edit'
    }

    const viewPersona = async (instance) => {
      persona.value = instance
      view.value = 'view'
    }

    const cancelEdit = _ => {
      if (instanceRef) {
        Object.assign(instanceRef, previousValues)
      }
      view.value = 'list'
    }

    const updatePagination = (newPagination, total) => {
      const { page, rowsPerPage, sortBy, descending } = newPagination
      pagination.value.page = page
      pagination.value.rowsPerPage = rowsPerPage
      pagination.value.sortBy = sortBy
      pagination.value.descending = descending
      pagination.value.rowsNumber = total
    }

    const onRequest = async (props) => {
      const { page, rowsPerPage, sortBy, descending } = props.pagination
      const filter = props.filter

      // Merge params in object for backend
      const paramsBackend = { page, rowsPerPage, sortBy, descending, jsondepth: 1 }

      // Init loading
      loading.value = true

      try {
        const response = await api.post('/search/persona', { id: filter }, { params: paramsBackend })
        // assign received rows
        rows.value = response.data.items
        // update local pagination object
        updatePagination(props.pagination, response.data.total)
      } catch (error) {
        $q.notify({
          type: 'negative',
          message: 'Ocurrió un error al obtener lista de persona'
        })
      } finally {
        // Finish loading
        loading.value = false
      }
    }

    const goToList = _ => {
      // Se redirecciona a la lista
      view.value = 'list'
      onRequest({
        pagination: pagination.value,
        filter: undefined
      })
    }

    const onSubmit = async () => {
      loading.value = true
      try {
        let message
        if (view.value === 'new') {
          await api.post('persona', persona.value)
          message = $t('page_added_correctly_message', { entity: $t('persona') })
        } else {
          await api.put(`persona/${persona.value.id}`, persona.value)
          message = $t('page_edited_correctly_message', { entity: $t('persona') })
        }
        $q.notify({ type: 'positive', message })
        goToList()
      } catch (error) {
        console.log(error)
        $q.notify({
          type: 'warning',
          message: $t('page_save_error_message', { entity: $t('persona') })
        })
      } finally {
        loading.value = false
      }
    }

    const onDelete = async () => {
      $q.dialog({
        title: $t('page_delete_dialog_title'),
        message: $t('page_delete_dialog_message', { entity: $t('persona') }),
        cancel: true,
        persistent: true
      }).onOk(async _ => {
        loading.value = true
        try {
          await api.delete(`persona/${persona.value.id}`)
          $q.notify({ type: 'positive', message: $t('page_delete_notify_message', { entity: $t('persona') }) })
          goToList()
        } catch (error) {
          console.log(error)
          $q.notify({
            type: 'warning',
            message: $t('page_delete_notify_error_message', { entity: $t('persona') })
          })
        } finally {
          loading.value = false
        }
      })
    }

    onMounted(async () => {
      onRequest({
        pagination: pagination.value,
        filter: undefined
      })
    })

    return {
      view,
      columns,
      rows,
      persona,
      loading,
      pagination,
      newPersona,
      editPersona,
      viewPersona,
      cancelEdit,
      onSubmit,
      onRequest,
      onDelete
    }
  }
}
</script>
