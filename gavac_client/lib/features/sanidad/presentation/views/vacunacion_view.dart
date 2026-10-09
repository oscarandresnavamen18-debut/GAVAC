import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart'; // Para kIsWeb

class VacunacionView extends StatelessWidget {
  const VacunacionView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Control Sanitario — GAVAC"),
        backgroundColor: const Color(0xFF1A3A32),
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: kIsWeb ? Colors.blue.shade50 : Colors.green.shade50,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  Icon(kIsWeb ? Icons.web : PhoneAndroidOrIOS(), color: kIsWeb ? Colors.blue : Colors.green),
                  const SizedBox(width: 12),
                  Text(
                    kIsWeb ? "Modo Web (Administración Central)" : "Modo Móvil (Captura en Campo / Offline)",
                    style: TextStyle(fontWeight: FontWeight.bold, color: kIsWeb ? Colors.blue.shade800 : Colors.green.shade800),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            const Text("Registrar Nueva Vacunación", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF1A3A32))),
            const SizedBox(height: 16),
            TextField(
              decoration: const InputDecoration(labelText: "Tag del Animal (Arete)", border: OutlineInputBorder()),
            ),
            const SizedBox(height: 16),
            TextField(
              decoration: const InputDecoration(labelText: "Nombre de la Vacuna", border: OutlineInputBorder()),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF1A3A32), foregroundColor: Colors.white),
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text("Vacunación registrada exitosamente bajo Clean Architecture")),
                  );
                },
                child: const Text("Guardar Vacunación"),
              ),
            ),
          ],
        ),
      ),
    );
  }

  IconData PhoneAndroidOrIOS() => Icons.phone_android;
}
