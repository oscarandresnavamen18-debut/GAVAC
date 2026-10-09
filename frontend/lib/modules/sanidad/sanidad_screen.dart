import 'package:flutter/material.dart';
import '../../shared/api_client.dart';

class SanidadScreen extends StatefulWidget {
  const SanidadScreen({super.key});

  @override
  State<SanidadScreen> createState() => _SanidadScreenState();
}

class _SanidadScreenState extends State<SanidadScreen> {
  List<dynamic> _sanidadList = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchSanidad();
  }

  void _fetchSanidad() async {
    try {
      final data = await ApiClient.get("/api/sanidad/");
      setState(() {
        _sanidadList = data;
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
      appBar: AppBar(title: const Text("Control Sanitario"), backgroundColor: const Color(0xFF1A3A32), foregroundColor: Colors.white),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(24.0),
              child: ListView.builder(
                itemCount: _sanidadList.length,
                itemBuilder: (context, index) {
                  final item = _sanidadList[index];
                  return Card(
                    child: ListTile(
                      leading: const CircleAvatar(backgroundColor: Color(0xFF1A3A32), child: Icon(Icons.healing, color: Colors.white)),
                      title: Text("Tratamiento: ${item['tipo_tratamiento']}"),
                      subtitle: Text("Diagnóstico: ${item['diagnostico']} • Costo: \$${item['costo'] ?? 0}"),
                    ),
                  );
                },
              ),
            ),
    );
  }
}
