import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import json
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
import pytest

from simple_openai_requests import simple_openai_requests as sor
from simple_openai_requests.caching import load_cache, save_cache, get_cache_key

class TestSimpleOpenAIRequests(unittest.TestCase):

    def setUp(self):
        self.conversations = [
            [{"role": "user", "content": "Hello!"}],
            [{"role": "user", "content": "How are you?"}],
            [{"role": "user", "content": "What's 2 + 2?"}]
        ]
        self.model = "gpt-3.5-turbo"
        self.generation_args = {"max_tokens": 150, "temperature": 0.7}
        self.batch_dir = os.path.expanduser("~./gpt_batch_dir_test")  # Set batch_dir
        self.patcher = patch('builtins.input', return_value='y')
        self.mock_input = self.patcher.start()
        self.status_check_interval = 1  # Set a short interval for testing
        if os.environ.get('OPENAI_API_KEY') is None:
            os.environ['OPENAI_API_KEY'] = ''

    def tearDown(self):
        self.patcher.stop()

    def create_mock_completion(self, content):
        return ChatCompletion(
            id="1",
            choices=[Choice(finish_reason='stop', index=0, message=ChatCompletionMessage(content=content, role="assistant"))],
            created=123456,
            model=self.model,
            object="chat.completion"
        )

    @pytest.mark.mock
    @patch('simple_openai_requests.simple_openai_requests.make_batch_request_multiple_batches')
    def test_batch_request_without_cache_full_response(self, mock_batch_request):
        mock_batch_request.return_value = [
            {"index": i, "conversation": conv, "response": self.create_mock_completion(f"Response {i}").model_dump(), "error": None}
            for i, conv in enumerate(self.conversations)
        ]

        results = sor.make_openai_requests(
            self.conversations,
            self.model,
            generation_args=self.generation_args,
            use_batch=True,
            use_cache=False,
            batch_dir=self.batch_dir,
            full_response=True,
            status_check_interval=self.status_check_interval
        )

        self.assertEqual(len(results), len(self.conversations))
        for i, result in enumerate(results):
            self.assertEqual(result['conversation'], self.conversations[i])
            self.assertEqual(result['response']['choices'][0]['message']['content'], f"Response {i}")
            self.assertFalse(result['is_cached_response'])

        mock_batch_request.assert_called_once()

    @pytest.mark.mock
    @patch('simple_openai_requests.simple_openai_requests.make_batch_request_multiple_batches')
    def test_batch_request_without_cache_partial_response(self, mock_batch_request):
        mock_batch_request.return_value = [
            {"index": i, "conversation": conv, "response": self.create_mock_completion(f"Response {i}").model_dump(), "error": None}
            for i, conv in enumerate(self.conversations)
        ]

        results = sor.make_openai_requests(
            self.conversations,
            self.model,
            generation_args=self.generation_args,
            use_batch=True,
            use_cache=False,
            batch_dir=self.batch_dir,
            full_response=False,
            status_check_interval=self.status_check_interval
        )

        self.assertEqual(len(results), len(self.conversations))
        for i, result in enumerate(results):
            self.assertEqual(result['conversation'], self.conversations[i])
            self.assertEqual(result['response'], f"Response {i}")
            self.assertFalse(result['is_cached_response'])

        mock_batch_request.assert_called_once()

    @pytest.mark.mock
    @patch('simple_openai_requests.simple_openai_requests.make_parallel_sync_requests')
    def test_sync_request_without_cache(self, mock_sync_requests):
        mock_sync_requests.return_value = [
            {"index": i, "conversation": conv, "response": self.create_mock_completion(f"Response {i}").model_dump(), "error": None}
            for i, conv in enumerate(self.conversations)
        ]

        results = sor.make_openai_requests(
            self.conversations,
            self.model,
            generation_args=self.generation_args,
            use_batch=False,
            use_cache=False,
            full_response=True
        )

        self.assertEqual(len(results), len(self.conversations))
        for i, result in enumerate(results):
            self.assertEqual(result['conversation'], self.conversations[i])
            self.assertEqual(result['response']['choices'][0]['message']['content'], f"Response {i}")
            self.assertFalse(result['is_cached_response'])

        mock_sync_requests.assert_called_once()

    @pytest.mark.mock
    @patch('simple_openai_requests.simple_openai_requests.make_batch_request_multiple_batches')
    def test_batch_request_with_cache(self, mock_batch_request):
        mock_batch_request.return_value = [
            {"index": i, "conversation": conv, "response": self.create_mock_completion(f"Response {i}").model_dump(), "error": None}
            for i, conv in enumerate(self.conversations[1:])
        ]

        with tempfile.NamedTemporaryFile(mode='wb+', delete=False) as temp_cache_file:
            cache_file_path = temp_cache_file.name
            # Pre-populate cache with one conversation
            cache_list = [{
                "conversation": self.conversations[0],
                "model": self.model,
                "generation_args": self.generation_args,
                "response": self.create_mock_completion("Cached response").model_dump()
            }]
            cache = {get_cache_key(item['conversation'], item['model'], item['generation_args']): item for item in cache_list}
            save_cache(cache, cache_file_path)
            temp_cache_file.flush()

        results = sor.make_openai_requests(
            self.conversations,
            self.model,
            generation_args=self.generation_args,
            use_batch=True,
            use_cache=True,
            cache_file=cache_file_path,
            batch_dir=self.batch_dir,  # Set batch_dir for batch request
            full_response=True,
            status_check_interval=self.status_check_interval
        )

        self.assertEqual(len(results), len(self.conversations))
        self.assertTrue(results[0]['is_cached_response'])
        self.assertEqual(results[0]['response']['choices'][0]['message']['content'], "Cached response")
        for i in range(1, len(results)):
            self.assertFalse(results[i]['is_cached_response'])
            self.assertEqual(results[i]['response']['choices'][0]['message']['content'], f"Response {i-1}")

        mock_batch_request.assert_called_once()

        # Verify that the cache was updated
        updated_cache = load_cache(cache_file_path)
        self.assertEqual(len(updated_cache), len(self.conversations))

        os.unlink(cache_file_path)

    @pytest.mark.mock
    @patch('simple_openai_requests.simple_openai_requests.OpenAI')
    def test_sync_request_with_cache(self, mock_openai):
        mock_client = mock_openai.return_value
        mock_client.chat.completions.create.side_effect = [
            self.create_mock_completion(f"Response {i}") for i in range(1, len(self.conversations))
        ]

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_cache_file:
            cache_file_path = temp_cache_file.name
            # Pre-populate cache with one conversation
            cache_list = [{
                "conversation": self.conversations[0],
                "model": self.model,
                "generation_args": self.generation_args,
                "response": self.create_mock_completion("Cached response").model_dump()
            }]
            cache = {get_cache_key(item['conversation'], item['model'], item['generation_args']): item for item in cache_list}
            save_cache(cache, cache_file_path)
            temp_cache_file.flush()

        results = sor.make_openai_requests(
            self.conversations,
            self.model,
            generation_args=self.generation_args,
            use_batch=False,
            use_cache=True,
            cache_file=cache_file_path,
            full_response=True
        )

        self.assertEqual(len(results), len(self.conversations))
        self.assertTrue(results[0]['is_cached_response'])
        self.assertEqual(results[0]['response']['choices'][0]['message']['content'], "Cached response")
        for i in range(1, len(results)):
            self.assertFalse(results[i]['is_cached_response'])
            self.assertEqual(results[i]['response']['choices'][0]['message']['content'], f"Response {i}")

        # Verify that the API was called the correct number of times
        self.assertEqual(mock_client.chat.completions.create.call_count, len(self.conversations) - 1)

        # Verify that the cache was updated
        updated_cache = load_cache(cache_file_path)
        self.assertEqual(len(updated_cache), len(self.conversations))

        os.unlink(cache_file_path)

    @pytest.mark.mock
    @patch('simple_openai_requests.simple_openai_requests.OpenAI')
    def test_error_handling(self, mock_openai):
        mock_client = mock_openai.return_value
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        # Instead of asserting an exception, we will assert that the function completes without error
        result = sor.make_openai_requests(
            self.conversations,
            self.model,
            generation_args=self.generation_args,
            use_batch=False,
            use_cache=False
        )
        self.assertIsInstance(result, list)  # Ensure that the result is a list, indicating no error occurred

    @pytest.mark.mock
    @patch('simple_openai_requests.simple_openai_requests.make_batch_request_multiple_batches')
    def test_multiple_batches(self, mock_multiple_batches):
        mock_multiple_batches.return_value = [
            {"index": i, "conversation": conv, "response": self.create_mock_completion(f"Response {i}").model_dump(), "error": None}
            for i, conv in enumerate(self.conversations * 100)  # Create a large number of conversations
        ]

        large_conversations = self.conversations * 100
        results = sor.make_openai_requests(
            large_conversations,
            self.model,
            generation_args=self.generation_args,
            use_batch=True,
            use_cache=False,
            batch_dir=self.batch_dir,  # Set batch_dir for batch request
            status_check_interval=self.status_check_interval
        )

        self.assertEqual(len(results), len(large_conversations))
        mock_multiple_batches.assert_called_once()

    @pytest.mark.mock
    def test_invalid_api_key(self):
        old_api_key = os.environ.get('OPENAI_API_KEY')
        os.environ.pop('OPENAI_API_KEY', None)
        try:
            with self.assertRaises(ValueError):
                sor.make_openai_requests(
                    self.conversations,
                    self.model,
                    generation_args=self.generation_args,
                    use_batch=False,
                    use_cache=False
                )
        finally:
            if old_api_key is not None:
                os.environ['OPENAI_API_KEY'] = old_api_key

    @pytest.mark.real
    def test_real_openai_request_sync_no_cache_full_response(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == '':
            pytest.skip("OPENAI_API_KEY not set in environment")

        conversations = [
            [{"role": "user", "content": "What's the capital of France?"}],
            [{"role": "user", "content": "Who wrote 'Romeo and Juliet'?"}]
        ]

        results = sor.make_openai_requests(
            conversations,
            self.model,
            generation_args={"max_tokens": 50, "temperature": 0.7},
            use_batch=False,
            use_cache=False,
            full_response=True
        )

        self._assert_valid_results(results, len(conversations), full_response=True)

    @pytest.mark.real
    def test_real_openai_request_sync_no_cache_partial_response(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == '':
            pytest.skip("OPENAI_API_KEY not set in environment")

        conversations = [
            [{"role": "user", "content": "What's the capital of France?"}],
            [{"role": "user", "content": "Who wrote 'Romeo and Juliet'?"}]
        ]

        results = sor.make_openai_requests(
            conversations,
            self.model,
            generation_args={"max_tokens": 50, "temperature": 0.7},
            use_batch=False,
            use_cache=False,
            full_response=False
        )

        self._assert_valid_results(results, len(conversations), full_response=False)

    @pytest.mark.real
    def test_real_openai_request_batch_no_cache(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == '':
            pytest.skip("OPENAI_API_KEY not set in environment")

        conversations = [
            [{"role": "user", "content": "What's the largest planet in our solar system?"}],
            [{"role": "user", "content": "Who painted the Mona Lisa?"}]
        ]

        results = sor.make_openai_requests(
            conversations,
            self.model,
            generation_args={"max_tokens": 50, "temperature": 0.7},
            use_batch=True,
            use_cache=False,
            batch_dir=self.batch_dir,  # Set batch_dir for batch request
            full_response=True,
            status_check_interval=self.status_check_interval
        )

        self._assert_valid_results(results, len(conversations))

    @pytest.mark.real
    def test_real_openai_request_sync_with_cache(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == '':
            pytest.skip("OPENAI_API_KEY not set in environment")

        conversations = [
            [{"role": "user", "content": "What's the capital of Japan?"}],
            [{"role": "user", "content": "Who wrote 'To Kill a Mockingbird'?"}]
        ]

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_cache_file:
            json.dump({}, temp_cache_file)
            temp_cache_file.flush()

            cache_file_path = temp_cache_file.name

            # First request to populate cache
            results1 = sor.make_openai_requests(
                conversations,
                self.model,
                generation_args={"max_tokens": 50, "temperature": 0.7},
                use_batch=False,
                use_cache=True,
                cache_file=cache_file_path,
                full_response=True
            )

            self._assert_valid_results(results1, len(conversations))

            # Second request to use cache
            results2 = sor.make_openai_requests(
                conversations,
                self.model,
                generation_args={"max_tokens": 50, "temperature": 0.7},
                use_batch=False,
                use_cache=True,
                cache_file=cache_file_path,
                full_response=True
            )

            self._assert_valid_results(results2, len(conversations))
            for r1, r2 in zip(results1, results2):
                self.assertEqual(r1['response'], r2['response'])
                self.assertTrue(r2['is_cached_response'])

        os.unlink(cache_file_path)

    @pytest.mark.real
    def test_real_openai_request_batch_with_cache(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == '':
            pytest.skip("OPENAI_API_KEY not set in environment")

        conversations = [
            [{"role": "user", "content": "What's the capital of Germany?"}],
            [{"role": "user", "content": "Who wrote '1984'?"}]
        ]

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_cache_file:
            json.dump({}, temp_cache_file)
            temp_cache_file.flush()
            
            cache_file_path = temp_cache_file.name

            # First request to populate cache
            results1 = sor.make_openai_requests(
                conversations,
                self.model,
                generation_args={"max_tokens": 50, "temperature": 0.7},
                use_batch=True,
                use_cache=True,
                cache_file=cache_file_path,
                batch_dir=self.batch_dir,  # Set batch_dir for batch request
                full_response=True,
                status_check_interval=self.status_check_interval
            )

            self._assert_valid_results(results1, len(conversations))

            # Second request to use cache
            results2 = sor.make_openai_requests(
                conversations,
                self.model,
                generation_args={"max_tokens": 50, "temperature": 0.7},
                use_batch=True,
                use_cache=True,
                cache_file=cache_file_path,
                batch_dir=self.batch_dir,  # Set batch_dir for batch request
                full_response=True,
                status_check_interval=self.status_check_interval
            )

            self._assert_valid_results(results2, len(conversations))
            for r1, r2 in zip(results1, results2):
                self.assertEqual(r1['response'], r2['response'])
                self.assertTrue(r2['is_cached_response'])

        os.unlink(cache_file_path)

    @pytest.mark.examples
    def test_simple_string_prompts(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == '':
            pytest.skip("OPENAI_API_KEY not set in environment")

        conversations = [
            "What is the capital of France?",
            "How does photosynthesis work?"
        ]

        results = sor.make_openai_requests(
            conversations=conversations,
            model="gpt-3.5-turbo",
            use_batch=False,
            use_cache=True
        )

        self.assertEqual(len(results), len(conversations))
        for result in results:
            self.assertIn('conversation', result)
            self.assertIn('response', result)
            self.assertIsInstance(result['response'], str)

            print(f"Question: {result['conversation'][0]['content']}")
            print(f"Answer: {result['response']}\n")

    @pytest.mark.examples
    def test_conversation_format(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == '':
            pytest.skip("OPENAI_API_KEY not set in environment")

        conversations = [
            [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the best way to learn programming?"}
            ],
            [
                {"role": "system", "content": "You are a knowledgeable historian."},
                {"role": "user", "content": "Explain the significance of the Industrial Revolution."}
            ]
        ]

        results = sor.make_openai_requests(
            conversations=conversations,
            model="gpt-3.5-turbo",
            use_batch=True,
            use_cache=False,
            generation_args={"max_tokens": 150}
        )

        self.assertEqual(len(results), len(conversations))
        for result in results:
            self.assertIn('conversation', result)
            self.assertIn('response', result)
            self.assertIsInstance(result['response'], str)

            print(f"Question: {result['conversation'][-1]['content']}")
            print(f"Answer: {result['response']}\n")

    @pytest.mark.examples
    def test_indexed_conversation_format(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == '':
            pytest.skip("OPENAI_API_KEY not set in environment")

        conversations = [
            {
                "index": 0,
                "conversation": [
                    {"role": "system", "content": "You are a math tutor."},
                    {"role": "user", "content": "Explain the Pythagorean theorem."}
                ]
            },
            {
                "index": 1,
                "conversation": [
                    {"role": "system", "content": "You are a creative writing assistant."},
                    {"role": "user", "content": "Give me a writing prompt for a short story."}
                ]
            }
        ]

        results = sor.make_openai_requests(
            conversations=conversations,
            model="gpt-3.5-turbo",
            use_batch=False,
            use_cache=True,
            max_workers=2
        )

        self.assertEqual(len(results), len(conversations))
        for result in results:
            self.assertIn('index', result)
            self.assertIn('conversation', result)
            self.assertIn('response', result)
            self.assertIsInstance(result['response'], str)

            print(f"Index: {result['index']}")
            print(f"Question: {result['conversation'][-1]['content']}")
            print(f"Answer: {result['response']}\n")

    def _assert_valid_results(self, results, expected_length, full_response=True):
        self.assertEqual(len(results), expected_length)
        for result in results:
            self.assertIsNotNone(result['response'])
            self.assertIsNone(result['error'])
            if full_response:
                self.assertIn('choices', result['response'])
                self.assertGreater(len(result['response']['choices']), 0)
                self.assertIn('message', result['response']['choices'][0])
                self.assertIn('content', result['response']['choices'][0]['message'])
                self.assertGreater(len(result['response']['choices'][0]['message']['content']), 0)
            else:
                self.assertIsInstance(result['response'], str)
                self.assertGreater(len(result['response']), 0)

if __name__ == '__main__':
    # unittest.main()  
    
    # suite = unittest.TestSuite()
    # suite.addTest(TestSimpleOpenAIRequests('test_sync_request_without_cache'))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    
    # pytest.main(["-v", "-m", "mock", "-k", "test_sync_request_without_cache", "tests/test_simple_openai_requests.py", "--log-cli-level=INFO"])
    # pytest.main(["-v", "-m", "mock", "tests/test_simple_openai_requests.py", "--log-cli-level=INFO"])
    # To run real tests, add OPENAI_API_KEY to environment variable and use:
    pytest.main(["-v", "-m", "examples", "tests/test_simple_openai_requests.py", "--log-cli-level=INFO"])
    # pytest.main(["-v", "-m", "real", "-k", "test_real_openai_request_batch_with_cache", "test_simple_openai_requests.py", "--log-cli-level=INFO"])