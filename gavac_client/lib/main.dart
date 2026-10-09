import 'package:flutter/material.dart';
import 'features/sanidad/presentation/views/vacunacion_view.dart';

void main() {
  runApp(const GavacApp());
}

class GavacApp extends StatelessWidget {
  const GavacApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GAVAC — Gestión Ganadera Inteligente',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1A3A32)),
        useMaterial3: true,
      ),
      home: const VacunacionView(),
    );
  }
}
