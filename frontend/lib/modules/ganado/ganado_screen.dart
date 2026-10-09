import 'package:flutter/material.dart';
import '../../shared/api_client.dart';

class GanadoScreen extends StatefulWidget {
  const GanadoScreen({super.key});

  @override
  State<GanadoScreen> createState() => _GanadoScreenState();
}

class _GanadoScreenState extends State<GanadoScreen> {
  List<dynamic> _animales = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchAnimales();
  }

  void _fetchAnimales() async {
    try {
      final data = await ApiClient.get("/api/ganado/");
      setState(() {
        _animales = data;
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
      appBar: AppBar(title: const Text("Inventario de Ganado"), backgroundColor: const Color(0xFF1A3A32), foregroundColor: Colors.white),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(24.0),
              child: ListView.builder(
                itemCount: _animales.length,
                itemBuilder: (context, index) {
                  final animal = _animales[index];
                  return Card(
                    child: ListTile(
                      leading: const CircleAvatar(backgroundColor: Color(0xFF1A3A32), child: Icon(Icons.pets, color: Colors.white)),
                      title: Text("Tag: ${animal['tag']} (${animal['nombre'] ?? 'Sin nombre'})"),
                      subtitle: Text("Raza: ${animal['raza'] ?? 'N/A'} • Peso: ${animal['peso_actual'] ?? 0} Kg • Lote: ${animal['lote'] ?? 'N/A'}"),
                      trailing: Text(animal['status'], style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.green)),
                    ),
                  );
                },
              ),
            ),
    );
  }
}
