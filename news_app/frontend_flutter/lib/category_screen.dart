import 'package:flutter/material.dart';
import 'api_service.dart';
import 'news_card.dart';

class CategoryScreen extends StatelessWidget {
  final ApiService apiService;
  final String category;
  const CategoryScreen({super.key, required this.apiService, required this.category});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(category.toUpperCase())),
      body: FutureBuilder<List<NewsItem>>(
        future: apiService.fetchByCategory(category),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }

          return PageView.builder(
            scrollDirection: Axis.vertical,
            itemCount: snapshot.data!.length,
            itemBuilder: (context, index) => NewsCard(item: snapshot.data![index]),
          );
        },
      ),
    );
  }
}
