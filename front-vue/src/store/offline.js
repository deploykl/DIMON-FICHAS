export default {
  namespaced: true,
  state: {
    queue: [],
    isOffline: false,
    syncInProgress: false
  },
  mutations: {
    ADD_TO_QUEUE(state, payload) {
      state.queue.push(payload);
    },
    REMOVE_FROM_QUEUE(state, id) {
      state.queue = state.queue.filter(item => item.id !== id);
    },
    SET_OFFLINE_MODE(state, status) {
      state.isOffline = status;
    },
    SET_SYNC_PROGRESS(state, status) {
      state.syncInProgress = status;
    }
  },
  actions: {
    async addToQueue({ commit, state }, request) {
      // Si ya existe una solicitud similar, no la agregues de nuevo
      const existingRequest = state.queue.find(
        item => item.url === request.url && 
                item.method === request.method && 
                JSON.stringify(item.data) === JSON.stringify(request.data)
      );
      
      if (existingRequest) return;

      const requestWithId = {
        ...request,
        id: Date.now(),
        timestamp: new Date().toISOString(),
        retries: 0
      };
      
      commit('ADD_TO_QUEUE', requestWithId);
      
      // Guardar en IndexedDB para persistencia
      try {
        if (window.indexedDB) {
          await this._vm.$offlineDB.addRequest(requestWithId);
        }
      } catch (error) {
        console.error('Error saving to IndexedDB:', error);
      }
    },
    async removeFromQueue({ commit }, id) {
      commit('REMOVE_FROM_QUEUE', id);
      
      try {
        if (window.indexedDB) {
          await this._vm.$offlineDB.removeRequest(id);
        }
      } catch (error) {
        console.error('Error removing from IndexedDB:', error);
      }
    },
    setOfflineMode({ commit }, status) {
      commit('SET_OFFLINE_MODE', status);
    },
    async loadQueueFromDB({ commit }) {
      if (!window.indexedDB) return;
      
      try {
        const requests = await this._vm.$offlineDB.getRequests();
        commit('SET_QUEUE', requests);
      } catch (error) {
        console.error('Error loading queue from DB:', error);
      }
    },
    async syncOfflineData({ state, commit, dispatch }) {
      if (state.syncInProgress || !state.queue.length) return;
      
      commit('SET_SYNC_PROGRESS', true);
      
      try {
        // Primero sincroniza las solicitudes en memoria
        for (const request of [...state.queue]) {
          try {
            const response = await this._vm.$api({
              method: request.method,
              url: request.url,
              data: request.data,
              headers: request.headers
            });
            
            await dispatch('removeFromQueue', request.id);
          } catch (error) {
            console.error('Failed to sync request:', request.url, error);
            request.retries += 1;
            
            // Si ha fallado demasiadas veces, quítala de la cola
            if (request.retries > 3) {
              await dispatch('removeFromQueue', request.id);
            }
          }
        }
        
        // Luego verifica si hay más en IndexedDB
        const dbRequests = await this._vm.$offlineDB.getRequests();
        for (const request of dbRequests) {
          if (!state.queue.some(item => item.id === request.id)) {
            try {
              const response = await this._vm.$api({
                method: request.method,
                url: request.url,
                data: request.data,
                headers: request.headers
              });
              
              await this._vm.$offlineDB.removeRequest(request.id);
            } catch (error) {
              console.error('Failed to sync DB request:', request.url, error);
            }
          }
        }
      } finally {
        commit('SET_SYNC_PROGRESS', false);
      }
    }
  },
  getters: {
    queue: state => state.queue,
    isOffline: state => state.isOffline,
    pendingRequestsCount: state => state.queue.length,
    syncInProgress: state => state.syncInProgress
  }
};