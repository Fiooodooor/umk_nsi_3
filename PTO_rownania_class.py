class StringParser:
	@staticmethod
	def check_is_tuple(a) -> bool:
		return isinstance(a, type((int, int)))

	@staticmethod
	def calculate_nwd(a: int, b: int) -> int:
		if a == 0 or b == 0:
			return 1
		while a != b:
			if a > b:
				a -= b
			else:
				b -= a
		return a

	def get_nwd_pair(self, numerator: int, denominator: int) -> (int, int):
		if denominator == 0:
			raise ZeroDivisionError("get_nwd_pair: Got tuple with denominator == 0! Error!")
		temp_nwd = self.calculate_nwd(abs(numerator), abs(denominator))
		return numerator // temp_nwd, denominator // temp_nwd

	def single_input_string_parse(self, string_input: str) -> []:
		output_stack = []
		operator_stack = []
		last_c = '('
		i = 0
		n = len(string_input)
		while i < n:
			c = string_input[i]
			i += 1
			if (c == '-' and last_c in ['(', '|']) or c.isdecimal():
				begin = i-1
				while i < n and string_input[i].isdecimal():
					i += 1
				if last_c == '|':
					output_stack.append(self.get_nwd_pair(output_stack.pop(), int(string_input[begin:i])))
				else:
					output_stack.append(int(string_input[begin:i]))
			elif c in ['(', '+', '-', '*', '/']:
				if c in ['+', '-']:
					while operator_stack and operator_stack[-1] != '(':
						output_stack.append(operator_stack.pop())
				elif c in ['/', '*']:
					while operator_stack and operator_stack[-1] not in ['(', '+', '-']:
						output_stack.append(operator_stack.pop())
				operator_stack.append(c)
			elif c == ')':
				while operator_stack and operator_stack[-1] != '(':
					output_stack.append(operator_stack.pop())
				if operator_stack and operator_stack[-1] == '(':
					operator_stack.pop()
				else:
					raise SyntaxError("single_input_string_parse: Unpaired bracket ')'! Reached end of stack and no '(' found!")
			elif c != '|':
				raise SyntaxError("single_input_string_parse: Unexpected symbol found! No support for:'" + c + "' character.")
			last_c = c
		while operator_stack:
			if operator_stack[-1] == '(':
				raise SyntaxError("single_input_string_parse: Unpaired bracket '('! It should not have been here!")
			output_stack.append(operator_stack.pop())
		return output_stack

	def single_input_onp_calculate(self, onp_stack: []) -> (int, int):
		temp_stack = []
		onp_stack.reverse()
		while onp_stack:
			itr = onp_stack.pop()
			if self.check_is_tuple(itr):
				temp_stack.append(itr)
			elif itr in ['+', '-', '/', '*']:
				b = temp_stack.pop()
				a = temp_stack.pop()
				switcher = {
					ord('+'): self.get_nwd_pair(a[0]*b[1]+b[0]*a[1], a[1]*b[1]),
					ord('-'): self.get_nwd_pair(a[0]*b[1]-b[0]*a[1], a[1]*b[1]),
					ord('*'): self.get_nwd_pair(a[0]*b[0], a[1]*b[1]),
					ord('/'): self.get_nwd_pair(a[0]*b[1], a[1]*b[0])
				}
				temp_stack.append(switcher.get(ord(itr)))
			else:
				raise SyntaxError("single_input_onp_calculate: Unknown symbol in onp_stack found!")
		if temp_stack:
			if len(temp_stack) > 1:
				raise SyntaxError("single_input_onp_calculate: len(temp_stack) > 1 ! Expecting 1 value which is the result.")
			return temp_stack.pop()
		raise SyntaxError("single_input_onp_calculate: temp_stack is empty! Expecting 1 value which is the result.")

	def parse_multiline_string(self, multiline: str) -> []:
		result_tuples = []
		try:
			single_lines_array = multiline.split('\n')
			for string_line in single_lines_array:
				onp_symbols_line = self.single_input_string_parse(string_line)
				tmp_result_tuple = self.single_input_onp_calculate(onp_symbols_line)
				result_tuples.append(tmp_result_tuple)
		except(IndexError, ZeroDivisionError, SyntaxError):
			result_tuples.append("Niepoprawne wyrazenie, liczba poprawnie obliczonych wyrazen: " + str(len(result_tuples)))
		finally:
			for res in result_tuples:
				print(res)
			return result_tuples


if __name__ == "__main__":
	multiline_input = "2|1+4|1*5|2-18|5\n(2|1+4|1)*5|2-18|5\ncztery * 5"
	parser = StringParser()
	result = parser.parse_multiline_string(multiline_input)
	exit(0)
