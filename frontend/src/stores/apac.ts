import { defineStore } from 'pinia';
import api from '../services/api';

export interface TermoEncontrado {
  termo: string;
  categoria: string;
  codigo_procedimento: string | null;
  cid_principal: string | null;
  cid_secundario: string | null;
  inicio: number;
  fim: number;
}

export interface PacienteApac {
  seq_atendimento: string | number;
  cns_paciente: string;
  nome_paciente: string;
  data_atendimento: string;
  texto_evolucao: string;
  termos_encontrados: TermoEncontrado[];
}

export const useApacStore = defineStore('apac', {
  state: () => ({
    pacientes: [] as PacienteApac[],
    loading: false,
    error: null as string | null,
  }),
  getters: {
    pacientesComStatus: (state) => {
      return state.pacientes.map(p => ({
        ...p,
        status: p.termos_encontrados && p.termos_encontrados.length > 0 ? 'PRONTA' : 'PENDENTE'
      }));
    }
  },
  actions: {
    async fetchPacientes() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get('/api/apac/pacientes');
        this.pacientes = response.data;
      } catch (err: any) {
        this.error = err.message || 'Erro ao carregar pacientes';
      } finally {
        this.loading = false;
      }
    },
    async adicionarTermo(termoData: any) {
      try {
        await api.post('/api/apac/dicionario', termoData);
        // Recarregar os pacientes para reprocessar a varredura
        await this.fetchPacientes();
      } catch (err: any) {
        this.error = err.message || 'Erro ao adicionar termo';
        throw err;
      }
    },
    async exportarTxt() {
      try {
        const response = await api.get('/api/apac/exportar');
        return response.data;
      } catch (err: any) {
        this.error = err.message || 'Erro ao exportar txt';
        throw err;
      }
    }
  }
});
