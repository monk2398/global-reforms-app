import 'dart:convert';
import 'package:http/http.dart' as http;

class NewsItem {
  final int id;
  final String title;
  final String summary;
  final String category;
  final String imageUrl;

  NewsItem({required this.id, required this.title, required this.summary, required this.category, required this.imageUrl});

  factory NewsItem.fromJson(Map<String, dynamic> json) {
    return NewsItem(
      id: json['id'],
      title: json['title'],
      summary: json['summary'],
      category: json['category'],
      imageUrl: json['image_url'],
    );
  }
}

class ApiService {
  final String baseUrl;
  ApiService({this.baseUrl = 'http://10.0.2.2:8000'});

  Future<List<NewsItem>> fetchLatest() async {
    final response = await http.get(Uri.parse('$baseUrl/news/latest'));
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((e) => NewsItem.fromJson(e)).toList();
  }

  Future<List<NewsItem>> fetchByCategory(String category) async {
    final response = await http.get(Uri.parse('$baseUrl/news/category/$category'));
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((e) => NewsItem.fromJson(e)).toList();
  }
}
