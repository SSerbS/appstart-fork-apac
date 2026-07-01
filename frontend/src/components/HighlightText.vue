<template>
  <div class="relative">
    <div 
      class="whitespace-pre-wrap font-mono text-sm p-4 border rounded bg-white text-gray-800"
      @mouseup="handleSelection"
      v-html="highlightedText"
    ></div>

    <!-- Modal para novo termo -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded shadow-lg w-96">
        <h3 class="text-lg font-bold mb-4">Adicionar Novo Termo</h3>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Jargão Médico (Selecionado)</label>
          <input type="text" v-model="novoTermo.jargao_medico" disabled class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm bg-gray-100 p-2" />
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Categoria</label>
          <div class="flex items-center space-x-4">
            <label class="inline-flex items-center">
              <input type="radio" v-model="novoTermo.categoria" value="diagnostico" class="form-radio text-indigo-600 focus:ring-indigo-500" />
              <span class="ml-2 text-sm text-gray-700">Diagnóstico/Morfologia</span>
            </label>
            <label class="inline-flex items-center">
              <input type="radio" v-model="novoTermo.categoria" value="tratamento" class="form-radio text-indigo-600 focus:ring-indigo-500" />
              <span class="ml-2 text-sm text-gray-700">Tratamento/Conduta</span>
            </label>
          </div>
        </div>
        <div v-if="novoTermo.categoria === 'tratamento'" class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Código do Procedimento (SIGTAP)</label>
          <input type="text" v-model="novoTermo.codigo_procedimento" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2" />
        </div>
        <div v-if="novoTermo.categoria === 'diagnostico'" class="mb-4">
          <label class="block text-sm font-medium text-gray-700">CID Principal</label>
          <input type="text" v-model="novoTermo.cid_principal" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm border p-2" />
        </div>
        <div class="flex justify-end space-x-2 mt-6">
          <button @click="showModal = false" class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">Cancelar</button>
          <button @click="salvarTermo" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Salvar Termo</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useApacStore } from '../stores/apac';

const props = defineProps<{
  textoEvolucao: string;
  termosEncontrados: any[];
}>();

const store = useApacStore();

const showModal = ref(false);
const novoTermo = ref({
  jargao_medico: '',
  categoria: 'diagnostico',
  codigo_procedimento: '',
  cid_principal: '',
  cid_secundario: ''
});

const highlightedText = computed(() => {
  if (!props.textoEvolucao) return '';
  if (!props.termosEncontrados || props.termosEncontrados.length === 0) return escapeHtml(props.textoEvolucao);


  
  // Abordagem segura construindo chunks
  let result = '';
  let lastIndex = 0;
  // Ordena do início para o fim
  const termosCrescente = [...props.termosEncontrados].sort((a, b) => a.inicio - b.inicio);
  
  for (const termo of termosCrescente) {
    if (termo.inicio > lastIndex) {
      result += escapeHtml(props.textoEvolucao.substring(lastIndex, termo.inicio));
    }
    const meio = escapeHtml(props.textoEvolucao.substring(termo.inicio, termo.fim));
    const title = termo.categoria === 'diagnostico' ? `Diagnóstico: CID ${termo.cid_principal}` : `Tratamento: Proc ${termo.codigo_procedimento}`;
    result += `<mark class="bg-green-300 text-black px-1 rounded cursor-help" title="${title}">${meio}</mark>`;
    lastIndex = termo.fim;
  }
  
  if (lastIndex < props.textoEvolucao.length) {
    result += escapeHtml(props.textoEvolucao.substring(lastIndex));
  }

  return result;
});

function escapeHtml(unsafe: string) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

const handleSelection = () => {
  const selection = window.getSelection();
  if (selection && selection.toString().trim() !== '') {
    novoTermo.value.jargao_medico = selection.toString().trim().toLowerCase();
    novoTermo.value.categoria = 'diagnostico';
    novoTermo.value.codigo_procedimento = '';
    novoTermo.value.cid_principal = '';
    showModal.value = true;
    
    selection.removeAllRanges();
  }
};

const salvarTermo = async () => {
  if (novoTermo.value.categoria === 'diagnostico' && !novoTermo.value.cid_principal) {
    alert('Preencha o CID principal.');
    return;
  }
  if (novoTermo.value.categoria === 'tratamento' && !novoTermo.value.codigo_procedimento) {
    alert('Preencha o código do procedimento (SIGTAP).');
    return;
  }
  
  // Enviar nulo para os campos da categoria que não foi selecionada
  const payload = {
    ...novoTermo.value,
    codigo_procedimento: novoTermo.value.categoria === 'tratamento' ? novoTermo.value.codigo_procedimento : null,
    cid_principal: novoTermo.value.categoria === 'diagnostico' ? novoTermo.value.cid_principal : null,
    cid_secundario: null
  };

  await store.adicionarTermo(payload);
  showModal.value = false;
};
</script>
