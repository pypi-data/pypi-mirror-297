import torch
import numpy as np
import pandas as pd
from torch import optim
from pathlib import Path
from typing import Union, List, Tuple, Collection
from sklearn.model_selection import train_test_split
from torch.nn import functional as F
from torch.optim.lr_scheduler import LRScheduler
from torch.utils.data import DataLoader, Dataset

from nlpx.llm import TokenizeVec
from nlpx.dataset import TokenDataset, PaddingTokenCollator
from nlpx.text_token import BaseTokenizer, PaddingTokenizer, SimpleTokenizer, Tokenizer, TokenEmbedding
from nlpx.training import Trainer, SimpleTrainer, ClassTrainer, SimpleClassTrainer, SplitClassTrainer, evaluate, \
	EvalClassTrainer, EvalSimpleClassTrainer


class ModelWrapper:
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import ModelWrapper
	>>> model_wrapper = ModelWrapper()
	>>> model_wrapper.train(model, train_set, val_set, collate_fn)
	>>> model_wrapper.logits(X_test)
	"""
	
	def __init__(self, model_path: Union[str, Path] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		self.device = device
		self.model = torch.load(model_path, map_location=device) if model_path else None
	
	def train(self, model, train_set: Dataset, collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, num_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, show_progress=False):
		trainer = Trainer(max_iter, optimizer, scheduler, learning_rate, T_max,
		                  batch_size,
		                  num_workers,
		                  pin_memory, pin_memory_device,
		                  persistent_workers,
		                  early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
		                  print_per_rounds,
		                  self.device)
		self.model = trainer.train(model, train_set, collate_fn, show_progress)
	
	def logits(self, X: torch.Tensor):
		self.model.eval()
		with torch.no_grad():
			logits = self.model(X)
		return logits
	
	def save(self, model_path: Union[str, Path] = './best_model.pt'):
		torch.save(self.model, model_path)
	
	def load(self, model_path: Union[str, Path] = './best_model.pt'):
		self.model = torch.load(model_path, map_location=self.device)


class SimpleModelWrapper(ModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import SimpleModelWrapper
	>>> model_wrapper = SimpleModelWrapper()
	>>> model_wrapper.train(model, X, y, collate_fn)
	>>> model_wrapper.logits(X_test)
	"""
	
	def __init__(self, model_path: Union[str, Path] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(model_path, device)
	
	def train(self, model, X: Union[torch.Tensor, np.ndarray, List], y: Union[torch.LongTensor, np.ndarray, List],
	          collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, num_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, show_progress=False):
		trainer = SimpleTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
		                        batch_size,
		                        num_workers,
		                        pin_memory, pin_memory_device,
		                        persistent_workers,
		                        early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
		                        print_per_rounds,
		                        self.device)
		self.model = trainer.train(model, X, y, collate_fn, show_progress)


class ClassModelWrapper(ModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import ClassModelWrapper
	>>> model_wrapper = ClassModelWrapper(classes=classes)
	>>> model_wrapper.train(model, train_set, val_set, collate_fn)
	>>> model_wrapper.predict(X_test)
	>>> model_wrapper.evaluate(test_set)
	"""
	
	def __init__(self, model_path: Union[str, Path] = None, classes: Collection[str] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		self.classes = classes
		self.device = device
		self.model = torch.load(model_path, map_location=device) if model_path else None
	
	def train(self, model, train_set: Dataset, val_set: Dataset = None, collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, show_progress=False):
		if val_set:
			trainer = EvalClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                           batch_size, eval_batch_size,
			                           num_workers, num_eval_workers,
			                           pin_memory, pin_memory_device,
			                           persistent_workers,
			                           early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
			                           print_per_rounds,
			                           self.device)
			self.model = trainer.train(model, train_set, val_set, collate_fn, show_progress)
		else:
			trainer = ClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                       batch_size, num_workers,
			                       pin_memory, pin_memory_device,
			                       persistent_workers,
			                       early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
			                       print_per_rounds,
			                       self.device)
			self.model = trainer.train(model, train_set, collate_fn, show_progress)
	
	def predict(self, X: torch.Tensor):
		logits = self.logits(X)
		return logits.argmax(-1)
	
	def predict_classes(self, X: torch.Tensor):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(X)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, X: torch.Tensor):
		logits = self.logits(X)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values.numpy()
	
	def predict_classes_proba(self, X: torch.Tensor):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(X)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values
	
	def evaluate(self, val_set: Dataset, batch_size=64, num_workers=0, collate_fn=None):
		val_loader = DataLoader(dataset=val_set, batch_size=batch_size, num_workers=num_workers, collate_fn=collate_fn)
		_, acc = evaluate(self.model, val_loader, self.device)
		return acc


class SimpleClassModelWrapper(ClassModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import SimpleClassModelWrapper
	>>> model_wrapper = SimpleClassModelWrapper(classes=classes)
	>>> model_wrapper.train(model, X, y val_data, collate_fn)
	>>> model_wrapper.predict(X_test)
	>>> model_wrapper.evaluate(X_test, y_test)
	"""
	
	def __init__(self, model_path: Union[str, Path] = None, classes: Collection[str] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(model_path, classes, device)
	
	def train(self, model, X: Union[torch.Tensor, np.ndarray, List], y: Union[torch.LongTensor, np.ndarray, List],
	          val_data: Tuple[Union[torch.Tensor, np.ndarray, List], Union[torch.LongTensor, np.ndarray, List]] = None,
	          collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, show_progress=False):
		if val_data:
			trainer = EvalSimpleClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                                 batch_size, eval_batch_size,
			                                 num_workers, num_eval_workers,
			                                 pin_memory, pin_memory_device,
			                                 persistent_workers,
			                                 early_stopping_rounds,
			                                 print_per_rounds,
			                                 self.device)
			self.model = trainer.train(model, X, y, val_data, collate_fn, show_progress)
		else:
			trainer = SimpleClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                             batch_size, num_workers,
			                             pin_memory, pin_memory_device,
			                             persistent_workers,
			                             early_stopping_rounds,
			                             print_per_rounds,
			                             self.device)
			self.model = trainer.train(model, X, y, collate_fn, show_progress)
	
	def evaluate(self, X: Union[torch.Tensor, np.ndarray, List], y: Union[torch.LongTensor, np.ndarray, List],
	             batch_size=64, num_workers=0, collate_fn=None):
		if isinstance(X, (List, np.ndarray)):
			X = torch.tensor(X, dtype=torch.float)
		if isinstance(y, (List, np.ndarray)):
			y = torch.tensor(y, dtype=torch.long)
			
		data_set = TokenDataset(X, y)
		return super().evaluate(data_set, batch_size, num_workers, collate_fn)


class TextModelWrapper(SimpleClassModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import TextModelWrapper
	>>> model_wrapper = TextModelWrapper(tokenize_vec, classes=classes)
	>>> model_wrapper.train(model, train_texts, y_train val_data, collate_fn)
	>>> model_wrapper.predict(test_texts)
	>>> model_wrapper.evaluate(test_texts, y_test)
	"""
	
	def __init__(self, tokenize_vec: Union[
		BaseTokenizer, PaddingTokenizer, SimpleTokenizer, Tokenizer, TokenizeVec, TokenEmbedding],
	             model_path: Union[str, Path] = None, classes: Collection[str] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(model_path, classes, device)
		self.tokenize_vec = tokenize_vec
	
	def train(self, model, texts: Union[Collection[str], np.ndarray, pd.Series],
	          y: Union[torch.LongTensor, np.ndarray, List],
	          val_data: Tuple[
		          Union[Collection[str], np.ndarray, pd.Series], Union[torch.LongTensor, np.ndarray, List]] = None,
	          max_length: int = None, collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, n_jobs=-1, show_progress=False):
		X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
		if val_data:
			val_data = (self.get_vec(val_data[0], max_length=max_length, n_jobs=-1), val_data[1])
		super().train(model, X, y, val_data, collate_fn, max_iter, optimizer, scheduler, learning_rate, T_max,
		              batch_size, eval_batch_size, num_workers, num_eval_workers, pin_memory, pin_memory_device,
		              persistent_workers, early_stopping_rounds, print_per_rounds, show_progress)
	
	def predict(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		logits = self.logits(texts, max_length, n_jobs=n_jobs)
		return logits.argmax(-1)
	
	def predict_classes(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(texts, max_length, n_jobs=n_jobs)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		logits = self.logits(texts, max_length, n_jobs=n_jobs)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values.numpy()
	
	def predict_classes_proba(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(texts, max_length, n_jobs)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values
	
	def logits(self, texts: Collection[str], max_length: int = None, n_jobs=-1):
		X = self.get_vec(texts, max_length, n_jobs=n_jobs)
		return super().logits(X)
	
	def evaluate(self, texts: Union[str, Collection[str], np.ndarray, pd.Series],
	             y: Union[torch.LongTensor, np.ndarray, List], batch_size=64, num_workers=0,
	             max_length: int = None, collate_fn=None, n_jobs=-1):
		X = self.get_vec(texts, max_length, n_jobs=n_jobs)
		if isinstance(y, (np.ndarray, List)):
			y = torch.tensor(y, dtype=torch.long)
		return super().evaluate(X, y, batch_size=batch_size, num_workers=num_workers, collate_fn=collate_fn)
	
	def get_vec(self, texts: Union[str, Collection[str], np.ndarray, pd.Series], max_length: int, n_jobs: int):
		if isinstance(texts, str):
			texts = [texts]
		
		if isinstance(self.tokenize_vec, TokenizeVec):
			return self.tokenize_vec.parallel_encode_plus(texts, max_length=max_length, padding='max_length',
			                                              truncation=True, add_special_tokens=True,
			                                              return_token_type_ids=True, return_attention_mask=True,
			                                              return_tensors='pt', n_jobs=n_jobs)
		
		elif isinstance(self.tokenize_vec, (PaddingTokenizer, SimpleTokenizer, Tokenizer)):
			return torch.LongTensor(self.tokenize_vec.batch_encode(texts, max_length))
		
		elif isinstance(self.tokenize_vec, TokenEmbedding):
			return self.tokenize_vec(texts, max_length)
		
		raise ValueError("Invalid tokenize_vec, it must be a TokenizeVec or TokenEmbedding.")


class SplitTextModelWrapper(TextModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import SplitTextModelWrapper
	>>> model_wrapper = SplitTextModelWrapper(tokenize_vec, classes=classes)
	>>> model_wrapper.train(model, texts, y, collate_fn)
	>>> model_wrapper.predict(test_texts)
	>>> model_wrapper.evaluate(test_texts, y_test)
	"""
	
	def __init__(self, tokenize_vec: Union[
		BaseTokenizer, PaddingTokenizer, SimpleTokenizer, Tokenizer, TokenizeVec, TokenEmbedding],
	             model_path: Union[str, Path] = None, classes: Collection[str] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(tokenize_vec, model_path, classes, device)
	
	def train(self, model, texts: Union[Collection[str], np.ndarray, pd.Series],
	          y: Union[torch.LongTensor, np.ndarray, List],
	          max_length: int = None, eval=True, val_size=0.2, random_state=None, collate_fn=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, n_jobs=-1, show_progress=False):
		X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
		if eval:
			trainer = SplitClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                            batch_size, eval_batch_size,
			                            num_workers, num_eval_workers,
			                            pin_memory, pin_memory_device,
			                            persistent_workers,
			                            early_stopping_rounds,
			                            print_per_rounds,
			                            self.device)
			self.model = trainer.train(model, X, y, val_size, random_state, collate_fn, show_progress)
		else:
			trainer = SimpleClassTrainer(max_iter, optimizer, scheduler, learning_rate, T_max,
			                             batch_size, num_workers,
			                             pin_memory, pin_memory_device,
			                             persistent_workers,
			                             early_stopping_rounds,
			                             print_per_rounds,
			                             self.device)
			self.model = trainer.train(model, X, y, collate_fn, show_progress)


class PaddingTextModelWrapper(ClassModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import PaddingTextModelWrapper
	>>> model_wrapper = PaddingTextModelWrapper(tokenizer, classes=classes)
	>>> model_wrapper.train(model, train_texts, y_train val_data)
	>>> model_wrapper.predict(test_texts)
	>>> model_wrapper.evaluate(test_texts, y_test)
	"""
	
	def __init__(self, tokenizer: Union[PaddingTokenizer, SimpleTokenizer, Tokenizer],
	             model_path: Union[str, Path] = None,
	             classes: Collection[str] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(model_path, classes, device)
		self.tokenizer = tokenizer
	
	def train(self, model, texts: Union[Collection[str], np.ndarray, pd.Series],
	          y: Union[torch.LongTensor, np.ndarray, List],
	          val_data: Tuple[Union[Collection[str], np.ndarray, pd.Series], Union[torch.LongTensor, np.ndarray, List]] = None,
	          max_length: int = None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, show_progress=False):
		X = self.tokenizer.batch_encode(texts, padding=False)
		train_set = TokenDataset(X, y)
		val_set = None
		if val_data:
			X_val = self.tokenizer.batch_encode(val_data[0], padding=False)
			val_set = TokenDataset(X_val, val_data[1])
		
		super().train(model, train_set, val_set, collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
		              max_iter=max_iter, optimizer=optimizer, scheduler=scheduler, learning_rate=learning_rate,
		              T_max=T_max, batch_size=batch_size, num_workers=num_workers, pin_memory=pin_memory,
		              pin_memory_device=pin_memory_device, persistent_workers=persistent_workers,
		              early_stopping_rounds=early_stopping_rounds, print_per_rounds=print_per_rounds,
		              show_progress=show_progress)
	
	def predict(self, texts: Collection[str], max_length: int = None):
		logits = self.logits(texts, max_length)
		return logits.argmax(-1)
	
	def predict_classes(self, texts: Collection[str], max_length: int = None):
		assert self.classes is not None, 'classes must be specified'
		pred = self.predict(texts, max_length)
		return [self.classes[i] for i in pred.detach().numpy().ravel()]
	
	def predict_proba(self, texts: Collection[str], max_length: int = None):
		logits = self.logits(texts, max_length)
		result = F.softmax(logits, dim=1).max(1)
		return result.indices, result.values.numpy()
	
	def predict_classes_proba(self, texts: Collection[str], max_length: int = None):
		assert self.classes is not None, 'classes must be specified'
		indices, values = self.predict_proba(texts, max_length)
		return [self.classes[i] for i in indices.detach().numpy().ravel()], values
	
	def logits(self, texts: Collection[str], max_length: int = None):
		X = self.tokenizer.batch_encode(texts, max_length)
		X = torch.tensor(X, dtype=torch.long)
		return super().logits(X)
	
	def evaluate(self, texts: Union[str, Collection[str], np.ndarray, pd.Series],
	             y: Union[torch.LongTensor, np.ndarray, List], batch_size=64, num_workers=0,
	             max_length: int = None):
		X = self.tokenizer.batch_encode(texts, padding=False)
		if isinstance(y, (np.ndarray, List)):
			y = torch.tensor(y, dtype=torch.long)
		val_set = TokenDataset(X, y)
		return super().evaluate(val_set, batch_size=batch_size, num_workers=num_workers,
		                        collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length))


class SplitPaddingTextModelWrapper(PaddingTextModelWrapper):
	"""
	Examples
	--------
	>>> from nlpx.model.wrapper import SplitPaddingTextModelWrapper
	>>> model_wrapper = SplitPaddingTextModelWrapper(tokenizer, classes=classes)
	>>> model_wrapper.train(model, texts, y)
	>>> model_wrapper.predict(test_texts)
	>>> model_wrapper.evaluate(test_texts, y_test)
	"""
	
	def __init__(self, tokenizer: Union[PaddingTokenizer, SimpleTokenizer, Tokenizer],
	             model_path: Union[str, Path] = None,
	             classes: Collection[str] = None,
	             device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')):
		super().__init__(tokenizer, model_path, classes, device)
	
	def train(self, model, texts: Union[Collection[str], np.ndarray, pd.Series],
	          y: Union[torch.LongTensor, np.ndarray, List],
	          max_length: int = None, eval=True, val_size=0.2, random_state=None, max_iter=100,
	          optimizer: Union[type, optim.Optimizer] = None, scheduler: LRScheduler = None,
	          learning_rate=0.001, T_max: int = 0,
	          batch_size=64, eval_batch_size=128,
	          num_workers=0, num_eval_workers=0,
	          pin_memory: bool = False, pin_memory_device: str = "",
	          persistent_workers: bool = False,
	          early_stopping_rounds: int = 10,
	          print_per_rounds: int = 1, show_progress=False):
		val_data = None
		if eval:
			X_train, X_test, y_train, y_test = train_test_split(texts, y, test_size=val_size, random_state=random_state)
			val_data = (X_test, y_test)
		else:
			X_train, y_train = texts, y
		
		super().train(model, X_train, y_train, val_data, max_length, max_iter, optimizer, scheduler, learning_rate,
		              T_max, batch_size, eval_batch_size, num_workers, num_eval_workers, pin_memory, pin_memory_device,
		              persistent_workers, early_stopping_rounds, print_per_rounds, show_progress)
