// src/utils/offlineDB.js
class OfflineDB {
  constructor() {
    this.dbName = 'OfflineRequestsDB';
    this.storeName = 'requests';
    this.db = null;
    this.initialize();
  }

  initialize() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);
      
      request.onerror = (event) => {
        console.error('Error opening IndexedDB:', event.target.error);
        reject(event.target.error);
      };
      
      request.onsuccess = (event) => {
        this.db = event.target.result;
        resolve(this.db);
      };
      
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'id' });
        }
      };
    });
  }

  async addRequest(request) {
    if (!this.db) await this.initialize();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(this.storeName, 'readwrite');
      const store = transaction.objectStore(this.storeName);
      
      const requestOp = store.add(request);
      
      requestOp.onsuccess = () => resolve();
      requestOp.onerror = (event) => {
        console.error('Error adding request:', event.target.error);
        reject(event.target.error);
      };
    });
  }

  async getRequests() {
    if (!this.db) await this.initialize();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(this.storeName, 'readonly');
      const store = transaction.objectStore(this.storeName);
      const request = store.getAll();
      
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = (event) => {
        console.error('Error getting requests:', event.target.error);
        reject(event.target.error);
      };
    });
  }

  async removeRequest(id) {
    if (!this.db) await this.initialize();
    
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction(this.storeName, 'readwrite');
      const store = transaction.objectStore(this.storeName);
      
      const requestOp = store.delete(id);
      
      requestOp.onsuccess = () => resolve();
      requestOp.onerror = (event) => {
        console.error('Error removing request:', event.target.error);
        reject(event.target.error);
      };
    });
  }
}

export default new OfflineDB();