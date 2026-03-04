import 'package:flutter/material.dart';
import 'api_service.dart';
import 'category_screen.dart';
import 'news_feed.dart';

void main() {
  runApp(const GeopoliticsNewsApp());
}

class GeopoliticsNewsApp extends StatelessWidget {
  const GeopoliticsNewsApp({super.key});

  @override
  Widget build(BuildContext context) {
    final apiService = ApiService();
    return MaterialApp(
      title: 'Global Reforms News',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF090B10),
        cardColor: const Color(0xFF1A1F2A),
        chipTheme: const ChipThemeData(backgroundColor: Color(0xFF2A3140)),
      ),
      home: HomeScreen(apiService: apiService),
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
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    final screens = [
      NewsFeed(apiService: widget.apiService),
      CategoryScreen(apiService: widget.apiService, category: 'geopolitics'),
      const Center(child: Text('Bookmarks coming soon')),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Global Reforms'),
        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8),
            child: Wrap(
              spacing: 6,
              children: ['geopolitics', 'defense', 'war', 'economy']
                  .map((category) => ChoiceChip(
                        label: Text(category),
                        selected: false,
                        onSelected: (_) => Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => CategoryScreen(apiService: widget.apiService, category: category),
                          ),
                        ),
                      ))
                  .toList(),
            ),
          )
        ],
      ),
      body: screens[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (value) => setState(() => _selectedIndex = value),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.newspaper), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.category), label: 'Category'),
          NavigationDestination(icon: Icon(Icons.bookmark), label: 'Bookmark'),
        ],
      ),
    );
  }
}
