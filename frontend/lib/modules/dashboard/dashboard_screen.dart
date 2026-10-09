import 'package:flutter/material.dart';
import '../ganado/ganado_screen.dart';
import '../sanidad/sanidad_screen.dart';
import '../admin/admin_screen.dart';
import '../auth/login_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  String _fincaNombre = "Cargando...";

  @override
  void initState() {
    super.initState();
    _loadFinca();
  }

  void _loadFinca() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _fincaNombre = prefs.getString('gavac_finca_nombre') ?? 'Finca Principal';
    });
  }

  void _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    if (mounted) {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => const LoginScreen()));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          // Sidebar Modular
          Container(
            width: 280,
            color: const Color(0xFF1A3A32),
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.shield_rounded, color: Colors.white, size: 28),
                    SizedBox(width: 12),
                    Text("GAVAC", style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: Colors.white)),
                  ],
                ),
                const SizedBox(height: 48),
                const Text("MENÚ PRINCIPAL", style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.white54, letterSpacing: 1.5)),
                const SizedBox(height: 16),
                _sidebarItem(Icons.dashboard, "Panel de Control", true, () {}),
                _sidebarItem(Icons.grid_view, "Inventario Ganado", false, () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => const GanadoScreen()));
                }),
                _sidebarItem(Icons.healing, "Control Sanitario", false, () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => const SanidadScreen()));
                }),
                const SizedBox(height: 32),
                const Text("SOPORTE Y ADMIN", style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.white54, letterSpacing: 1.5)),
                const SizedBox(height: 16),
                _sidebarItem(Icons.settings, "Administración", false, () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => const AdminScreen()));
                }),
                const Spacer(),
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red.shade900.withOpacity(0.2), foregroundColor: Colors.red.shade300),
                  onPressed: _logout,
                  icon: const Icon(Icons.logout, size: 16),
                  label: const Text("Cerrar Sesión"),
                ),
              ],
            ),
          ),
          // Main Content Area
          Expanded(
            child: Column(
              children: [
                // Topbar
                Container(
                  height: 80,
                  padding: const EdgeInsets.symmetric(horizontal: 32),
                  decoration: const BoxDecoration(color: Colors.white, border: Border(bottom: BorderSide(color: Color(0xFFF1F5F9)))),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        decoration: BoxDecoration(color: const Color(0xFFF8FAFC), borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFFE2E8F0))),
                        child: Row(
                          children: [
                            const Icon(Icons.location_on, size: 18, color: Color(0xFF1A3A32)),
                            const SizedBox(width: 8),
                            Text("Finca activa: $_fincaNombre", style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF1A3A32))),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                // Dashboard Body
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(32.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("Buenos días, Jairo", style: TextStyle(fontSize: 36, fontWeight: FontWeight.w900, color: Color(0xFF1A3A32))),
                        const SizedBox(height: 8),
                        const Text("Aquí tienes el estado biológico de tu hato hoy.", style: TextStyle(color: Colors.grey, fontSize: 16, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 32),
                        Row(
                          children: [
                            _kpiCard("Población Total", "1,248", Icons.grid_view, Colors.emerald),
                            const SizedBox(width: 24),
                            _kpiCard("En Sanidad", "12", Icons.healing, Colors.amber),
                            const SizedBox(width: 24),
                            _kpiCard("Reproducción", "45", Icons.favorite, Colors.blue),
                            const SizedBox(width: 24),
                            _kpiCard("Eficiencia", "88%", Icons.trending_up, Colors.purple),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _sidebarItem(IconData icon, String label, bool isActive, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(color: isActive ? Colors.white.withOpacity(0.1) : Colors.transparent, borderRadius: BorderRadius.circular(16)),
        child: Row(
          children: [
            Icon(icon, color: isActive ? Colors.white : Colors.white60, size: 20),
            const SizedBox(width: 14),
            Text(label, style: TextStyle(color: isActive ? Colors.white : Colors.white60, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  Widget _kpiCard(String title, String value, IconData icon, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(24), border: Border.all(color: const Color(0xFFF1F5F9))),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.between,
              children: [
                Icon(icon, color: const Color(0xFF1A3A32)),
                const Text("+2.4%", style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold, fontSize: 12)),
              ],
            ),
            const SizedBox(height: 16),
            Text(title.toUpperCase(), style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w900, color: Colors.grey, letterSpacing: 1.2)),
            const SizedBox(height: 8),
            Text(value, style: const TextStyle(fontSize: 32, fontWeight: FontWeight.w900, color: Color(0xFF1A3A32))),
          ],
        ),
      ),
    );
  }
}
