import 'package:flutter/material.dart';
import 'services/api_service.dart';
import 'models/animal.dart';

void main() {
  runApp(const GavacMobileApp());
}

class GavacMobileApp extends StatelessWidget {
  const GavacMobileApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GAVAC Mobile',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1A3A32)),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final ApiService _apiService = ApiService();
  bool _isLoading = false;
  String? _errorMsg;

  void _login() async {
    setState(() {
      _isLoading = true;
      _errorMsg = null;
    });

    try {
      bool success = await _apiService.login(
        _emailController.text.trim(),
        _passwordController.text,
      );

      if (success && mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => HomeScreen(apiService: _apiService)),
        );
      } else {
        setState(() {
          _errorMsg = "Credenciales incorrectas";
        });
      }
    } catch (e) {
      setState(() {
        _errorMsg = "Error de conexión: $e";
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF7F9F7),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Center(
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.shield_rounded, size: 80, color: Color(0xFF1A3A32)),
                const SizedBox(height: 16),
                const Text(
                  "GAVAC Mobile",
                  style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Color(0xFF1A3A32)),
                ),
                const Text("Gestión Ganadera Inteligente", style: TextStyle(color: Colors.grey)),
                const SizedBox(height: 32),
                TextField(
                  controller: _emailController,
                  decoration: const InputDecoration(labelText: "Correo Electrónico", border: OutlineInputBorder()),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: const InputDecoration(labelText: "Contraseña", border: OutlineInputBorder()),
                ),
                if (_errorMsg != null) ...[
                  const SizedBox(height: 12),
                  Text(_errorMsg!, style: const TextStyle(color: Colors.red)),
                ],
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF1A3A32),
                      foregroundColor: Colors.white,
                    ),
                    onPressed: _isLoading ? null : _login,
                    child: _isLoading ? const CircularProgressIndicator(color: Colors.white) : const Text("Acceder"),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  final ApiService apiService;
  const HomeScreen({super.key, required this.apiService});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late Future<List<Animal>> _futureAnimales;

  @override
  void initState() {
    super.initState();
    _futureAnimales = widget.apiService.listarAnimales();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Hato Ganadero (GAVAC Mobile)"),
        backgroundColor: const Color(0xFF1A3A32),
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder<List<Animal>>(
        future: _futureAnimales,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text("No hay animales registrados."));
          }

          final animales = snapshot.data!;
          return ListView.builder(
            itemCount: animales.length,
            itemBuilder: (context, index) {
              final animal = animales[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  leading: const CircleAvatar(backgroundColor: Color(0xFF1A3A32), child: Icon(Icons.pets, color: Colors.white)),
                  title: Text("Tag: ${animal.tag} (${animal.nombre ?? 'Sin nombre'})"),
                  subtitle: Text("Especie: ${animal.especie} • Raza: ${animal.raza ?? 'N/A'} • Peso: ${animal.pesoActual ?? 0} Kg"),
                  trailing: Text(animal.status, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.green)),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
