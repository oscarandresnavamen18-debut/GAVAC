import 'package:flutter/material.dart';
import '../../shared/api_client.dart';

class AdminScreen extends StatefulWidget {
  const AdminScreen({super.key});

  @override
  State<AdminScreen> createState() => _AdminScreenState();
}

class _AdminScreenState extends State<AdminScreen> {
  List<dynamic> _usuarios = [];
  List<dynamic> _fincas = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchAdminData();
  }

  void _fetchAdminData() async {
    try {
      final usuarios = await ApiClient.get("/api/admin/usuarios/");
      final fincas = await ApiClient.get("/api/admin/fincas/");
      setState(() {
        _usuarios = usuarios;
        _fincas = fincas;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Centro Administrativo"), backgroundColor: const Color(0xFF1A3A32), foregroundColor: Colors.white),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(24.0),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("Fincas de la Organización", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 16),
                        Expanded(
                          child: ListView.builder(
                            itemCount: _fincas.length,
                            itemBuilder: (context, index) {
                              final f = _fincas[index];
                              return Card(child: ListTile(title: Text(f['nombre']), subtitle: Text(f['ubicacion'] ?? 'Sin ubicación')));
                            },
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 24),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("Usuarios y Permisos", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 16),
                        Expanded(
                          child: ListView.builder(
                            itemCount: _usuarios.length,
                            itemBuilder: (context, index) {
                              final u = _usuarios[index];
                              return Card(child: ListTile(title: Text(u['email']), subtitle: Text("Rol: ${u['rol_organizacion']}")));
                            },
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
