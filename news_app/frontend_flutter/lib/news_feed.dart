import 'package:flutter/material.dart';
import 'api_service.dart';
import 'news_card.dart';

class NewsFeed extends StatefulWidget {
  final ApiService apiService;
  const NewsFeed({super.key, required this.apiService});

  @override
  State<NewsFeed> createState() => _NewsFeedState();
}

class _NewsFeedState extends State<NewsFeed> {
  late Future<List<NewsItem>> _newsFuture;

  @override
  void initState() {
    super.initState();
    _newsFuture = widget.apiService.fetchLatest();
  }

  Future<void> _refresh() async {
    setState(() {
      _newsFuture = widget.apiService.fetchLatest();
    });
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<NewsItem>>(
      future: _newsFuture,
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Center(child: CircularProgressIndicator());
        }

        final items = snapshot.data!;
        return RefreshIndicator(
          onRefresh: _refresh,
          child: PageView.builder(
            scrollDirection: Axis.vertical,
            itemCount: items.length,
            itemBuilder: (context, index) => NewsCard(item: items[index]),
          ),
        );
      },
    );
  }
}
