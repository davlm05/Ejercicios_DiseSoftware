import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:3000/amantes';

function App() {
  const [registro, setRegistro] = useState({ nombre: '', edad: '', intereses: '' });
  const [busqueda, setBusqueda] = useState('');
  const [resultados, setResultados] = useState([]);
  const [mensaje, setMensaje] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        nombre: registro.nombre,
        edad: parseInt(registro.edad),
        intereses: registro.intereses.split(',').map(i => i.trim())
      };
      await axios.post(API_URL, payload);
      setMensaje('Perfil registrado exitosamente!');
      setRegistro({ nombre: '', edad: '', intereses: '' });
      setTimeout(() => setMensaje(''), 3000);
    } catch (error) {
      setMensaje('Error al registrar: ' + (error.response?.data?.message || error.message));
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`${API_URL}?interes=${busqueda}`);
      setResultados(response.data.data);
    } catch (error) {
      setMensaje('Error en la búsqueda');
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Amante Ideal</h1>
        <p>Encuentra a tu pareja perfecta por intereses comunes</p>
      </header>

      {mensaje && (
        <div style={{ padding: '1rem', backgroundColor: '#334155', borderRadius: '8px', marginBottom: '2rem', textAlign: 'center' }}>
          {mensaje}
        </div>
      )}

      <div className="forms-container">
        <div className="card">
          <h2>Registrar Perfil</h2>
          <form onSubmit={handleRegister}>
            <div className="input-group">
              <label>Nombre</label>
              <input type="text" value={registro.nombre} onChange={e => setRegistro({...registro, nombre: e.target.value})} required />
            </div>
            <div className="input-group">
              <label>Edad</label>
              <input type="number" min="18" value={registro.edad} onChange={e => setRegistro({...registro, edad: e.target.value})} required />
            </div>
            <div className="input-group">
              <label>Intereses (separados por coma)</label>
              <input type="text" placeholder="Ej: viajar, leer, cine" value={registro.intereses} onChange={e => setRegistro({...registro, intereses: e.target.value})} required />
            </div>
            <button type="submit">Guardar Perfil</button>
          </form>
        </div>

        <div className="card">
          <h2>Buscar Candidatos</h2>
          <form onSubmit={handleSearch}>
            <div className="input-group">
              <label>Interés en común</label>
              <input type="text" placeholder="Ej: leer" value={busqueda} onChange={e => setBusqueda(e.target.value)} />
            </div>
            <button type="submit">Buscar</button>
          </form>

          <div className="results">
            {resultados.map(amante => (
              <div key={amante._id} className="amante-card">
                <h3>{amante.nombre}, {amante.edad}</h3>
                <div className="badges">
                  {amante.intereses.map((int, i) => (
                    <span key={i} className="badge">{int}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
