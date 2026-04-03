// frontend/static/app.js
function portfolioApp() {
  return {
    clients: [],
    selectedClientId: '',
    dashboard: null,
    loading: false,
    useMock: false,

    async init() {
      // Redirection si pas de token
      if (!localStorage.getItem('token')) {
        window.location.href = '/';
        return;
      }
      await this.loadClients();
    },

    headers() {
      return { 'Authorization': `Bearer ${localStorage.getItem('token')}` };
    },

    async loadClients() {
      try {
        const res = await fetch('/api/clients/', { headers: this.headers() });
        if (res.status === 401) { this.logout(); return; }
        this.clients = await res.json();
        // Sélectionner le premier client automatiquement
        if (this.clients.length > 0) {
          this.selectedClientId = this.clients[0].id;
          await this.loadDashboard();
        }
      } catch (e) { console.error('Erreur chargement clients:', e); }
    },

    async loadDashboard() {
      if (!this.selectedClientId) { this.dashboard = null; return; }
      this.loading = true;
      try {
        const url = `/api/dashboard/${this.selectedClientId}?mock=${this.useMock}`;
        const res = await fetch(url, { headers: this.headers() });
        if (res.ok) this.dashboard = await res.json();
      } catch (e) { console.error('Erreur dashboard:', e); }
      finally { this.loading = false; }
    },

    exportCsv() {
      if (!this.selectedClientId) return;
      const url = `/api/dashboard/${this.selectedClientId}/export/csv?mock=${this.useMock}`;
      // Téléchargement via lien temporaire
      const a = document.createElement('a');
      a.href = url;
      a.setAttribute('download', '');
      // Injecter le header Auth via fetch puis créer un blob
      fetch(url, { headers: this.headers() })
        .then(r => r.blob())
        .then(blob => {
          a.href = URL.createObjectURL(blob);
          a.click();
        });
    },

    logout() {
      localStorage.removeItem('token');
      window.location.href = '/';
    },

    fmt(val) {
      if (val == null) return '—';
      return new Intl.NumberFormat('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(val);
    }
  };
}