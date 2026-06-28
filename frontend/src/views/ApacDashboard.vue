<template>
  <div class="mb-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Dashboard APAC</h2>
      <button @click="exportar" class="px-4 py-2 bg-purple-600 text-white font-semibold rounded hover:bg-purple-700 transition shadow">
        Exportar APACs
      </button>
    </div>

    <div v-if="store.loading" class="text-center py-8 text-gray-500">
      Carregando pacientes...
    </div>
    
    <div v-else-if="store.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ store.error }}
    </div>

    <div v-else class="space-y-6">
      <div v-for="paciente in store.pacientesComStatus" :key="paciente.seq_atendimento" class="bg-white p-6 rounded shadow border border-gray-200">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 border-b pb-4">
          <div>
            <h3 class="text-xl font-bold text-gray-800">{{ paciente.nome_paciente }}</h3>
            <p class="text-sm text-gray-500">CNS: {{ paciente.cns_paciente }} | Data: {{ paciente.data_atendimento }}</p>
          </div>
          <div class="mt-2 md:mt-0">
            <span 
              class="px-3 py-1 rounded-full text-sm font-bold border"
              :class="paciente.status === 'PRONTA' ? 'bg-green-100 text-green-800 border-green-300' : 'bg-yellow-100 text-yellow-800 border-yellow-300'"
            >
              {{ paciente.status }}
            </span>
          </div>
        </div>

        <div>
          <h4 class="text-sm font-semibold mb-2 text-gray-700">Evolução Clínica:</h4>
          <p class="text-xs text-gray-500 mb-2 italic">Dica: Selecione um trecho do texto com o mouse para mapear um novo jargão.</p>
          <HighlightText 
            :textoEvolucao="paciente.texto_evolucao" 
            :termosEncontrados="paciente.termos_encontrados" 
          />
        </div>
      </div>
      
      <div v-if="store.pacientesComStatus.length === 0" class="text-center text-gray-500 py-8 bg-white rounded shadow border border-gray-200">
        Nenhum paciente encontrado.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useApacStore } from '../stores/apac';
import HighlightText from '../components/HighlightText.vue';

const store = useApacStore();

onMounted(() => {
  store.fetchPacientes();
});

const exportar = async () => {
  try {
    const txt = await store.exportarTxt();
    
    // Simula o download do TXT gerado
    const blob = new Blob([txt], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'apac_exportacao.txt';
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (e) {
    alert('Erro ao exportar TXT');
  }
};
</script>
