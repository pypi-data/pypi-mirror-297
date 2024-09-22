# -*- coding: utf-8 -*-
import win32com.client  # pywin32의 모듈
import jfinder, scolor, youtil  # xython 모듈
import basic_data
import copy
from xy_list import xy_list as xylist

class ganada:

	def __check_doc(self, file_name):
		"""
		다음줄, 다음단어의 의미 : 현재 기준에서 1을 한것
		단어의 시작 : 글자가 시작되는 지점에서 마지막 공백까지
		단어 : 문자열이 같은 형태의 묶음 (123가나다 => 공백이 없어도 2개단어)


		만약 오픈된 워드가 하나도 없으면,새로운 빈 워드를 만든다

		:param file_name: 입력한 화일 이름
		"""
		if file_name == "":
			# 만약 오픈된 워드가 하나도 없으면,새로운 빈 워드를 만든다
			try:
				self.doc = self.word_application.ActiveDocument
			except:
				self.doc = self.word_application.Documents.Add()
		elif file_name == "new":
			self.doc = self.word_application.Documents.Add()
		else:
			self.doc = self.word_application.Documents.Open(file_name)
			self.word_application.ActiveDocument.ActiveWindow.View.Type = 3

		self.selection = self.word_application.Selection
		self.range = self.doc.Range

	def __init__(self, file_name=""):
		"""
		현재 활성화된 워드의 모든 문단수 갖고온다
		형태적인 분류 : active_doc(화일) > sentence(문장) > word(한 단어) > character(한글자)
		의미적인 분류 : active_doc(화일) > paragraph(문단) > line(줄) > word(한 단어) > character(한글자)
		sentence : 표현이 완결된 단위, 그 자체로 하나의 서술된 문장이 되는 것
		paragraph : 줄바꿈이 이루어지기 전까지의 자료
		공통으로 사용할 변수들을 설정하는 것이다

		2024-04-27 : 전체적으로 이름을 terms에 따라서 변경함
		"""
		self.color = scolor.scolor()
		self.jf = jfinder.jfinder()
		self.util = youtil.youtil()

		self.vars = basic_data.basic_data().vars  # package안에서 공통적으로 사용되는 변수들

		# 워드 전체에 공통적으로 사용되는 변수
		self.common_range = None
		self.common_selection = None
		self.common_font_list = None
		self.x = None
		self.y = None
		self.font_dic = {}
		self.font_dic_default = {}
		self.letter_type_vs_enum = {"cell": 12, "char":1, "word":2, "line":5, "sentence" : 3, "para": 4,
							"character":1,"column":9,"item":16,"paragraph":4,"row":10,"section":8,"story":6,"table":15,
							"wdCell": 12, "wdColumn": 9, "wdRow": 10, "wdTable": 15, "wdCharacte": 1,"wdWord": 2,
							"wdCharacterFormatting": 13, "wdItem": 16, "wdLine": 5, "wdSentence": 3,"wdParagraph": 4,
							"wdParagraphFormatting": 14, "wdScreen": 7, "wdSection": 8, "wdStory": 6,"wdWindow": 11,
							}

		self.letter_type_dic = {"line": "line", "줄": "line", "한줄": "line", "라인": "line",
					"paragraph": "paragraph", "패러그래프": "paragraph", "문단": "paragraph", "para": "paragraph",
					"word": "word", "단어": "word", "워드": "word",
					"sentence": "sentence", "문장": "sentence",
					"char": "char", "글자": "char", "문자": "char","character": "char",
					"cell":"cell",
					"column": "column","col": "column",
					"row": "row",
					"item": "item",
					"셀": "cell", "컬럼": "column", "아이템": "item", "파라그래프": "paragraph",
					"파라": "paragraph", "가로": "row", "섹션": "section", "스토리": "story",
					"section": "section", "story": "story", "table": "table", "테이블": "table",
					}


		self.obj_word = {}  # 객체를 사용하기 위해서 사용하는것

		if file_name == "no" or file_name == "not":
			pass
		else:
			self.__start_ganada(file_name)

	def __start_ganada(self, file_name):
		# 워드를 실행시킵니다
		self.word_application = win32com.client.dynamic.Dispatch('Word.Application')
		self.word_application.Visible = 1
		self.selection = self.word_application.Selection

		self.__check_doc(file_name)

	def __str__(self):
		return self.doc

	def check_content_name(self, input_name):
		"""
		어떤 기준으로 할것인지를 확인하는 것
		content로 사용되는 단어들을 이것저것 사용하여도 적용이 가능하도록 만든것

		:param input_name:
		"""
		result = self.letter_type_dic[input_name]
		return result

	def check_font_style(self, *input_list):
		"""
		어떤 폰트의 속성이 오더라도 적용하게 만드는 것

		:param input_list:
		:return:
		"""
		check_bold = self.vars["check_bold"]
		check_italic = self.vars["check_italic"]
		check_underline = self.vars["check_underline"]
		check_breakthrough = self.vars["check_breakthrough"]
		check_alignment = self.vars["check_alignment"]
		for one in input_list:
			if one in check_bold.keys():
				self.font_dic["bold"] = True
			elif one in check_italic.keys():
				self.font_dic["italic"] = True
			elif one in check_underline.keys():
				self.font_dic["underline"] = True
			elif one in check_breakthrough.keys():
				self.font_dic["strikethrough"] = True
			elif one in check_alignment.keys():
				self.font_dic["align"] = self.vars["check_alignment"][one]
			elif type(one) == type(123) and one < 100:
				self.font_dic["size"] = one
			elif self.is_scolor_style(one):
				self.font_dic["color"] = self.color.change_scolor_to_rgbint(one)

	def check_letter_type(self, input_letter_type):
		"""
		글자의 형태를 확인하는 것

		:param input_letter_type:
		:return:
		"""
		result = self.letter_type_dic[input_letter_type]
		return result

	def check_letter_type_no(self, input_letter_type):
		"""
		사용하는 글자 묶음의 형태를 기본 형으로 바꾸는 것
		"""
		if type(input_letter_type) == type(123):
			result = input_letter_type
		else:
			result = self.letter_type_vs_enum[input_letter_type]
		return result

	def check_opend_file(self, input_file_name):
		doc_no = self.word_application.Documents.Count
		file_names = []
		for no in range(doc_no):
			file_names.append(self.word_application.Documents(no + 1).Name)

		if input_file_name in file_names:
			return True

		return False

	def check_range(self, input_range =""):
		if input_range != "":
			result = input_range
		else:
			if not self.range:
				result = self.word_application.Selection
			else:
				result = self.range
		return result

	def check_range_object(self, input_range_object=""):
		"""
		range와 selection을 함께 사용이 가능하도록 만드는 것

		:param input_range_object:
		"""
		if input_range_object == "":
			input_range_object = self.selection

		return input_range_object

	def check_table_object(self, table_object):
		"""
		숫자가 오면 index로 인식해서 테이블 객체를 찾아주는 것

		:param table_object:
		"""
		if type(table_object) == type(123):
			result = self.doc.Tables(table_object - 1)
		else:
			result = table_object
		return result

	def close(self):
		"""
		현재 활성화된 문서를 닫는다
		"""
		self.doc.Close()

	def close_all_doc_without_save(self):
		"""
		현재 활성화된 문서를 저장하지 않고 그냥 닫는다
		"""
		for one in self.word_application.Documents:
			one.Close(SaveChanges=False)

	def count_char_in_doc(self):
		"""
		문서안의 총 글자수 (공백도 1개의 글자이다)
		"""
		result = len(self.doc.Characters)
		return result

	def count_char_in_range(self):
		"""
		range안의 글자수 (공백도 1개의 글자이다)
		"""
		if not self.range:
			self.range = self.word_application.Selection

		x = self.range.Start
		y = self.range.End
		result = y - x
		return result

	def count_char_in_selection(self):
		"""
		선택영역안의 글자수 (공백도 1개의 글자이다)
		"""
		x = self.selection.Start
		y = self.selection.End
		result = y - x
		return result

	def count_doc(self):
		"""
		현재 열려져있는 화일의 모든 갯수를 갖고온다
		"""
		result = self.word_application.Documents.Count
		return result

	def count_line_in_doc(self):
		"""
		문서안의 총 줄수
		"""
		self.select_all()
		result = self.count_line_in_selection()
		return result

	def count_line_in_range(self, input_range=""):
		"""
		range안의 줄수
		ComputeStatistics의 입력숫자를 이용하여 선택영역의 정보를 갖고오는것 :
			예 : ComputeStatistics(3) :글자수
			3 :글자수, 0 :단어수, 1 :라인수, 4 :para수, 2 :page수

		"""
		input_range = self.check_range(input_range)
		len_line = input_range.ComputeStatistics(1)
		return len_line

	def count_line_in_selection(self):
		"""
		선택영역안의 줄수

		ComputeStatistics의 입력숫자를 이용하여 선택영역의 정보를 갖고오는것 :
			예 : ComputeStatistics(3) :글자수
			3 :글자수, 0 :단어수, 1 :라인수, 4 :para수, 2 :page수
		"""
		len_line = self.selection.Range.ComputeStatistics(1)
		return len_line

	def count_page_in_doc(self):
		"""
		문서안의 총 페이지 수
		"""
		result = self.doc.ComputeStatistics(2)
		return result

	def count_page_in_range(self, input_range=""):
		"""
		range안의 줄수

		ComputeStatistics(2) :영역안의 통계정보중 page수
		"""
		input_range = self.check_range(input_range)
		len_line = input_range.ComputeStatistics(2)
		return len_line

	def count_page_in_selection(self):
		"""
		선택영역안의 페이지수
		ComputeStatistics(2) :영역안의 통계정보중 page수
		"""
		len_page = self.selection.Range.ComputeStatistics(2)
		return len_page

	def count_para_in_doc(self):
		"""
		문서안의 종 문단수
		"""
		result = self.doc.Paragraphs.Count
		return result

	def count_para_in_range(self, input_range=""):
		"""
		range안의 문단수
		ComputeStatistics(4) :영역안의 통계정보중 para수
		"""
		input_range = self.check_range(input_range)
		len_para = input_range.ComputeStatistics(4)
		return len_para

	def count_para_in_selection(self):
		"""
		선택영역안의 문단수
		ComputeStatistics(4) :영역안의 통계정보중 para수
		"""
		len_para = self.selection.Range.ComputeStatistics(4)
		return len_para

	def count_table_in_doc(self):
		"""
		현재 워드화일안의 테이블의 총 갯수
		"""
		result = self.doc.Tables.Count
		return result

	def count_table_in_range(self, input_range=""):
		"""
		range안의 문단수
		"""
		input_range = self.check_range(input_range)
		result = input_range.Tables.Count
		return result

	def count_table_in_selection(self):
		"""
		현재 워드화일안의 테이블의 총 갯수
		"""
		result = self.selection.Tables.Count
		return result

	def count_word_in_doc(self):
		"""
		현재 워드화일안의 총단어숫자
		ComputeStatistics(0) :영역안의 통계정보중 단어수
		"""
		myrange = self.doc.StoryRanges(1)
		len_word = myrange.ComputeStatistics(0)
		return len_word

	def count_word_in_range(self, input_range=""):
		"""
		range안의 줄수
		ComputeStatistics(0) :영역안의 통계정보중 단어수
		"""
		input_range = self.check_range(input_range)
		result = input_range.ComputeStatistics(0)
		return result

	def count_word_in_selection(self):
		"""
		선택영역안의 단어수
		ComputeStatistics(0) :영역안의 통계정보중 단어수
		"""
		result = self.selection.Range.ComputeStatistics(0)
		return result


	def cut_range(self, input_range=""):
		"""
		range 영역 잘라내기
		"""
		input_range = self.check_range(input_range)
		input_range.Cut()

	def cut_selection(self):
		"""
		선택한 영역 잘라내기
		"""
		self.word_application.Selection.Cut()

	def delete_all_in_doc(self):
		"""
		문서안의 모든 것을 삭제하는 것
		"""
		self.selection.WholeStory()
		self.word_application.Selection.Delete()

	def delete_char_at_cursor(self):
		self.select_nth_char_from_start_of_doc(0)
		self.delete_selection()

	def delete_from_range_to_nth_char(self, input_no):
		self.delete_from_range_to_nth_letter_type("char", input_no)

	def delete_from_range_to_nth_letter_type(self, input_letter_type, input_no):
		"""
		글자의 종류에 따라서 range안의 n번째의 것을 삭제

		:param input_letter_type:
		:param input_no: 1부터시작하는 번호
		:return:
		"""
		current_range = self.get_current_range_object()
		self.expand_range_to_nth_letter_type(current_range, input_letter_type, input_no)
		self.delete_range()

	def delete_from_range_to_nth_line(self, input_no):
		self.delete_from_range_to_nth_letter_type("line", input_no)

	def delete_from_range_to_nth_para(self, input_no):
		self.delete_from_range_to_nth_letter_type("para", input_no)

	def delete_from_range_to_nth_word(self, input_no):
		self.delete_from_range_to_nth_letter_type("word", input_no)

	def delete_from_selection_to_nth_char(self, input_no):
		"""
		삭제 : 현재 선택된 영역의 끝에서 부터 n번째 글자까지
		:param input_no:
		"""
		self.delete_from_selection_to_nth_letter_type("char", input_no)

	def delete_from_selection_to_nth_letter_type(self, input_letter_type, input_no):
		self.select_from_selection_to_nth_letter_type(input_letter_type, input_no)
		self.word_application.Selection.range.Text = ""

	def delete_from_selection_to_nth_line(self, input_no):
		self.delete_from_selection_to_nth_letter_type("line", input_no)

	def delete_from_selection_to_nth_para(self, input_no=1):
		"""
		삭제 : 현재 선택된 영역의 끝에서 부터 n번째 문단까지
		:param input_no:
		"""
		self.delete_from_selection_to_nth_letter_type("para", input_no)

	def delete_from_selection_to_nth_word(self, input_no=1):
		"""
		삭제 : 현재 선택된 영역의 끝에서 부터 n번째 단어까지
		:param input_no: 1부터시작하는 번호
		"""
		self.delete_from_selection_to_nth_letter_type("word", input_no)

	def delete_from_start_of_doc_to_nth_char(self, input_no):
		"""
		삭제 : 문서 처음에서 n번째의 문자까지
		:param input_no:
		"""
		self.move_cursor_to_start_of_doc()
		self.delete_from_selection_to_nth_letter_type("char", input_no)

	def delete_from_start_of_doc_to_nth_letter_type(self, input_letter_type, input_no):
		self.move_cursor_to_start_of_doc()
		self.select_from_selection_to_nth_letter_type(input_letter_type, input_no)
		self.word_application.Selection.range.Text = ""

	def delete_from_start_of_doc_to_nth_line(self, input_no):
		"""
		삭제 : 문서 처음에서 n번째 라인까지
		:param input_no:
		"""
		self.move_cursor_to_start_of_doc()
		self.delete_from_selection_to_nth_letter_type("line", input_no)

	def delete_from_start_of_doc_to_nth_para(self, input_no):
		"""
		삭제 : 문서 처음에서 n번째 문단까지
		:param input_no:
		"""
		self.move_cursor_to_start_of_doc()
		self.delete_from_selection_to_nth_letter_type("para", input_no)

	def delete_from_start_of_doc_to_nth_sentence(self, input_no):
		self.select_nth_sentence_from_start_of_doc(input_no)
		self.delete_selection()

	def delete_from_start_of_doc_to_nth_word(self, input_no):
		"""
		삭제 : 문서 처음에서 n번째의 문자까지
		:param input_no:
		"""
		self.move_cursor_to_start_of_doc()
		self.delete_from_selection_to_nth_letter_type("word", input_no)

	def delete_line_at_cursor(self):
		self.select_nth_line_from_start_of_doc(0)
		self.delete_selection()

	def delete_nth_char_from_start_of_doc(self, input_no):
		self.move_cursor_to_nth_char_from_start_of_doc(input_no)
		self.delete_char_at_cursor()

	def delete_nth_line_from_start_of_doc(self, input_no):
		self.select_nth_line_from_start_of_doc(input_no)
		self.delete_selection()

	def delete_nth_para_from_start_of_doc(self, input_no):
		self.select_nth_para_from_start_of_doc(input_no)
		self.delete_selection()

	def delete_nth_shape_from_start_of_doc(self, input_no):
		"""
		n번째 그림객체 삭제

		:param input_no:
		"""
		pass

	def delete_nth_table_from_start_of_doc(self, input_no):
		"""
		n번째 테이블 삭제

		:param input_no: 1부터시작하는 번호
		"""
		self.doc.Tables(input_no-1).Delete()

	def delete_nth_word_from_start_of_doc(self, input_no):
		self.select_nth_word_from_start_of_doc(input_no)
		self.delete_selection()

	def delete_para_at_cursor(self):
		self.select_nth_para_from_start_of_doc(0)
		self.delete_selection()

	def delete_range(self):
		"""
		선택한 영역을 삭제
		"""
		self.doc.Range.Delete()

	def delete_selection(self):
		"""
		선택한 영역을 삭제
		"""
		self.word_application.Selection.Delete()

	def delete_sentence_at_cursor(self):
		self.select_nth_sentence_from_start_of_doc(0)
		self.delete_selection()

	def delete_word_at_cursor(self):
		self.select_nth_word_from_start_of_doc(0)
		self.delete_selection()

	def delete_xxline_in_table(self, table_obj, xx):
		"""
		현재 워드화일안의 테이블객체에서 가로행 번호를 이용하여 가로행을 삭제
		테이블의 가로행을 삭제

		:param table_obj: 테이블 객제
		:param xx: 가로행의 시작번호
		"""
		for no in range(xx[1] - xx[0]):
			table_obj.Rows(xx[0]).Delete()

	def delete_yyline_in_table(self, table_obj, yy):
		"""
		현재 워드화일안의 테이블객체에서 세로행 번호를 이용하여 세로행을 삭제

		:param table_obj:  테이블 객제
		:param yy:  세로행의 시작번호
		"""
		for no in range(yy[1] - yy[0]):
			table_obj.Columns(yy[0]).Delete()

	def draw_borderline_for_selection(self):
		"""
		선택영역의 외곽선 그리기
		"""
		self.selection.Font.Borders(1).LineStyle = 7  # wdLineStyleDouble	7
		self.selection.Font.Borders(1).LineWidth = 6  # wdLineWidth075pt	6
		self.selection.Font.Borders(1).ColorIndex = 7  # 7 :yellow

	def draw_line_color_for_table(self, table_obj, inside_color="bla", outside_color="bla"):
		"""
		테이블의 선을 색칠하기

		:param table_obj:  테이블 객제
		:param inside_color: 안쪽 색이름
		:param outside_color: 바깥쪽 색이름
		"""
		table_obj.Borders.InsideColorIndex = self.vars["color_index"][inside_color]
		table_obj.Borders.OutsideColorIndex = self.vars["color_index"][outside_color]

	def draw_line_style_for_table(self, table_obj, inside_line="-", outside_line="-"):
		"""
		테이블 선의 모양을 선정

		:param table_obj:  테이블 객제
		:param inside_line: 안쪽선의 모양
		:param outside_line: 바깥쪽 선의 모양
		"""
		table_obj.Borders.InsideLineStyle = self.vars["line"][inside_line]
		table_obj.Borders.OutsideLineStyle = self.vars["line"][outside_line]

	def draw_outline_for_selection(self):
		self.draw_borderline_for_selection()

	def draw_outside_border_for_selection(self, line_style=1, line_color="blu", line_width="+"):
		"""
		선택영역의 외곽선을 그리기

		:param line_style: 선의 스타일을 선택
		:param line_color: 선의 색을 선택
		:param line_width: 선의 두께를 선택
		"""
		self.selection.Borders.OutsideLineStyle = line_style
		self.selection.Borders.OutsideLineWidth = self.vars["word"]["line_width"][line_width]
		self.selection.Borders.OutsideColor = self.vars["word"]["color_24bit"][line_color]

	def expand_from_range_to_nth_letter_type(self, input_range, letter_type, input_no, except_current=False):
		"""
		선택영역을 입력형식에 맞도록 옮기는 것이다
		except_current : 현재 단어나 글자를 포함할것인지 아닌지를 선택하는 것이다
		에를 들어 2개를 원해도 현재것을 포함하면, 3개가 선택되어진다는 뜻입니다
		:param letter_type:
		:param input_no:
		:param except_current:
		:return:
		"""

		if input_range=="":
			input_range = self.word_application.Selection

		old_x = input_range.Start
		old_y = input_range.End
		letter_type_no = self.letter_type[letter_type]

		#다음것의 처음으로 이동하는 것이다
		if except_current:
			if input_no > 0:
				input_range.Move(letter_type_no, 1)
			else:
				input_range.Move(letter_type_no, -1)
			old_x = input_range.Start
			old_y = input_range.End


		input_range.Move(letter_type_no, input_no)
		new_x1 = input_range.Start
		new_x2 = input_range.Start

		#selection의 영역을 선택할때는 start, end를 사용한다
		input_range.Start = min(new_x1, new_x2,old_x, old_y)
		input_range.End = max(new_x1, new_x2, old_x, old_y)

		#print(input_range.Text)

	def expand_range_to_nth_char(self, input_range, input_no):
		new_range = self.expand_range_to_nth_letter_type(input_range, "char", input_no)
		return new_range

	def expand_range_to_nth_letter_type(self, input_range, letter_type, input_no):
		"""
		현재 range영역 + 입력형태의 끝까지 영역을 확장 하는 것

		현재 위치에서 원하는 문자의 형태 끝까지 영역을 확대 하는 것
		move : range객체의 start를 이동시키는 것,

		letter_type : 어떻게 이동을 하는지를 설정하는 것입니다
		input_no : +는 뒤로, -는 앞으로 이동한다
		"""

		# 기존의 자료를 저장한다

		if input_range=="":
			input_range = self.word_application.Selection

		old_x = input_range.Start
		old_y = input_range.End
		letter_type_no = self.vars["word"]["letter_type"][letter_type]

		if letter_type in ["char", "word", "line", "para"]:
			# 어떤 형태라도 range의 끝점을 이동시키는 것
			if input_no > 0:
				input_range.Move(letter_type_no, input_no)
				new_x1 = input_range.Start

				input_range.Move(letter_type_no, 1)
				new_x2 = input_range.Start
			else:
				input_range.Move(letter_type_no, input_no)
				new_x1 = input_range.Start
				input_range.Move(letter_type_no, -1)
				new_x2 = input_range.Start
				# print("값이 음수일때 --> ", old_x, old_y, new_x1, new_x2)
		#selection의 영역을 선택할때는 start, end를 사용한다
		self.selection.Start = min(new_x1, new_x2,old_x, old_y)
		self.selection.End = max(new_x1, new_x2, old_x, old_y)

	def expand_range_to_nth_letter_type_1(self, input_range, letter_type):
		"""
		현재 위치에서 원하는 문자의 형태 끝까지 영역을 확대 하는 것
		예를들어 한줄의 중간에서 이것을 이용하면, 줄의 중간에서 끝까지를 선택하는 것이다

		letter_type : 어떻게 이동을 하는지를 설정하는 것입니다
		input_no : +는 뒤로, -는 앞으로 이동한다
		#어떤 형태라도 range의 끝점을 이동시키는 것
		워드, 라인이나 para의 끝까지 이동하는 것
		"""
		input_range = self.check_range(input_range)

		letter_type_no = self.vars["word"]["letter_type"][letter_type]

		if letter_type in ["char", "word", "line", "para"]:
			input_range.EndOf(letter_type_no, 1)  # extend :1, move :0
		return input_range

	def expand_range_to_nth_line(self, input_range, input_no):
		new_range = self.expand_range_to_nth_letter_type(input_range, "line", input_no)
		return new_range

	def expand_range_to_nth_para(self, input_range, input_no):
		new_range = self.expand_range_to_nth_letter_type(input_range, "para", input_no)
		return new_range

	def expand_range_to_nth_word(self, input_range, input_no):
		new_range = self.expand_range_to_nth_letter_type(input_range, "word", input_no)
		return new_range

	def expand_selection_to_nth_char(self, input_no):
		self.select_from_selection_to_nth_letter_type("char", input_no)
		return self.selection

	def expand_selection_to_nth_letter_type(self, letter_type, input_no, except_current=False):
		"""
		선택영역을 입력형식에 맞도록 옮기는 것이다
		except_current : 현재 단어나 글자를 포함할것인지 아닌지를 선택하는 것이다
		에를 들어 2개를 원해도 현재것을 포함하면, 3개가 선택되어진다는 뜻입니다
		:param letter_type:
		:param input_no:
		:param except_current:
		:return:
		"""

		old_x = self.selection.Start
		old_y = self.selection.End
		letter_type_no = self.letter_type_vs_enum[letter_type]

		#다음것의 처음으로 이동하는 것이다
		if except_current:
			if input_no > 0:
				self.selection.Move(letter_type_no, 1)
			else:
				self.selection.Move(letter_type_no, -1)
			old_x = self.selection.Start
			old_y = self.selection.End


		self.selection.Move(letter_type_no, input_no)
		new_x1 = self.selection.Start
		new_x2 = self.selection.Start

		#selection의 영역을 선택할때는 start, end를 사용한다
		self.selection.Start = min(new_x1, new_x2,old_x, old_y)
		self.selection.End = max(new_x1, new_x2, old_x, old_y)

	def expand_selection_to_nth_line(self, input_no):
		self.select_from_selection_to_nth_letter_type("line", input_no)

	def expand_selection_to_nth_para(self, input_no):
		"""		현재 selection에서 n번째 para까지 선택		"""
		self.select_from_selection_to_nth_letter_type("para", input_no)

	def expand_selection_to_nth_word(self, input_no):
		"""		현재 selection에서 n번째 word까지 선택		"""
		self.select_from_selection_to_nth_letter_type("word", input_no)

	def find_first_text_in_selection_as_xy(self, search_text):
		"""
		현재 위치에서 찾는것을 입력하면, 바로 다음것을 선택하는 것
		search를 사용할것인지 find를 사용할것인지 정해보자
		replace

		:param search_text:
		"""
		result = []
		if self.selection.Find.Execute(search_text):
			self.selection.Range.Font.Italic = True
			self.selection.Range.Font.Color = 255
			self.selection.Range.HighlightColorIndex = 11
			start_no = self.selection.Range.Start
			end_no = start_no + len(search_text)
			temp = [start_no, end_no, self.selection.Range.Text]
			result.append(temp)

		return result

	def find_style_in_doc(self, input_style):
		result = []
		rng = self.doc.Range()
		rng.Find.IgnoreSpace = True
		rng.Find.Style = input_style
		while 1:
			ret = rng.Find.Execute()
			if not ret:
				return result
			result.append(ret)

	def find_text_all_in_doc_as_xy_list(self, search_text):
		"""
		1 : 워드 문서의 전체를 Range 로 만드는 것

		:param search_text:
		"""
		result = []
		myrange = self.doc.StoryRanges(1)  # 1
		myrange.Find.Text = search_text
		found_or_not = myrange.Find.Execute(Forward=True)
		while found_or_not:
			start_no = myrange.Start
			end_no = myrange.End
			# print("찾은 곳의 시작 위치 => ", start_no, "찾은 곳의 끝 위치 =>", end_no)
			result.append([start_no, end_no])
			found_or_not = myrange.Find.Execute(Forward=True)
		return result

	def find_text_all_in_doc_with_ignorespace(self, input_text):
		result = []
		rng = self.doc.Range()
		rng.Find.IgnoreSpace = True
		while 1:
			ret = rng.Find.Execute(input_text)
			if not ret:
				return result
			result.append(ret)
			start_no = rng.Start
			end_no = start_no + len(input_text)

	def find_text_all_in_range_as_xy_list(self, input_range, search_text, replace_text=False):
		"""
		:param search_text:
		"""
		result = []
		input_range.Find.Text = search_text
		if replace_text:
			input_range.Find.Replacement.Text = replace_text
		found_or_not = input_range.Find.Execute(Forward=True)
		while found_or_not:
			start_no = input_range.Start
			end_no = input_range.End
			# print("찾은 곳의 시작 위치 => ", start_no, "찾은 곳의 끝 위치 =>", end_no)
			result.append([start_no, end_no])
			found_or_not = input_range.Find.Execute(Forward=True)
		return result

	def find_text_all_in_selection_as_xy_list_with_colored(self, search_text):
		"""
		선택영역의 전체에서 입력글자를 찾아서 색깔을 넣기

		:param search_text:
		"""
		result = []
		while self.selection.Find.Execute(search_text):
			self.selection.Range.Font.Italic = True
			self.selection.Range.Font.Color = 255
			self.selection.Range.HighlightColorIndex = 11
			start_no = self.selection.Range.Start
			end_no = start_no + len(search_text)
			temp = [start_no, end_no, self.selection.Range.Text]
			result.append(temp)
		return result

	def get_active_doc_name(self):
		"""
		현재 활성화된 워드화일의 이름
		"""

		result = self.word_application.ActiveDocument.Name
		return result

	def get_bookmark_all_in_doc(self):
		"""
		북마크의 리스트를 돌려준다
		"""
		result = []
		for bookmark in self.doc.Bookmarks:
			bookmark_name = bookmark.Name
			my_range = self.doc.Bookmarks(bookmark.Name).Range
			my_range_text = my_range.Text
			start_no = my_range.Start
			end_no = my_range.End
			temp = [bookmark_name, start_no, end_no, my_range_text]
			result.append(temp)
		return result

	def get_char_no_for_end_of_selection(self):
		""" 선택영역의 끝글자 번호 """
		result = self.word_application.Selection.End
		return result

	def get_char_no_for_start_of_selection(self):
		""" 선택영역의 시작 문자 번호 """
		result = self.word_application.Selection.Start
		return result

	def get_current_range_object(self):
		my_range = self.doc.Range
		return my_range

	def get_doc_name_all(self):
		"""
		현재 열려있는 모든 문서의 이름을 돌려준다
		"""
		doc_no = self.word_application.Documents.Count
		result = []
		for no in range(doc_no):
			result.append(self.word_application.Documents(no + 1).Name)
		return result

	def get_first_table_index_in_selection(self):
		"""
		선택된 곳의 테이블의 index값을 갖고온다
		"""
		result = None
		if self.selection.Information(12) == False:
			pass
		else:
			IngStart = self.selection.Range.Start
			IngEnd = self.selection.Range.End
			self.selection.Collapse(Direction=1)
			self.selection.MoveEnd(Unit=1, Count=IngEnd - IngStart)
			tabnum = self.doc.Range(0, self.selection.Tables(1).Range.End).Tables.Count
			if self.selection.Cell.Count:
				result = tabnum
		return result

	def get_font_color_for_selection(self):
		"""
		선택영역의 글자색을 정하기
		"""
		result = self.selection.Font.Color
		return result

	def get_font_size_for_selection(self):
		"""
		선택영역의 글자크기 정하기
		"""
		result = self.selection.Font.Size
		return result

	def get_line_at_cursor(self):
		"""
		현재 커서의 시작 라인번호
		"""
		start_line_no_at_cursor = self.selection.Information(10)
		self.select_nth_line_from_start_of_doc(start_line_no_at_cursor)
		self.expand_selection_to_nth_line(1)
		return self.word_application.Selection.Text

	def get_line_no_for_end_of_selection(self):
		""" 선택영역의 끝줄 번호 """
		start_line = self.get_line_no_for_start_of_selection()
		len_line = self.selection.Range.ComputeStatistics(1)
		return start_line + len_line - 1

	def get_line_no_for_start_of_selection(self):
		""" 선택영역의 시작 줄 번호 """
		result = self.selection.Information(10)
		return result

	def get_line_no_for_start_of_selection_1(self):
		""" 선택영역의 시작 줄 번호 """
		x = self.word_application.Selection.Start
		y = self.word_application.Selection.End
		new_range = self.doc.Range(Start=0, End=y)

		result = new_range.Lines.Count
		return result

	def get_page_no_for_end_of_selection(self):
		""" 선택영역의 끝 페이지 번호 """
		result = self.selection.Information(3)
		return result

	def get_page_no_for_start_of_selection(self):
		""" 선택영역의 시작 페이지 번호 """
		result = self.selection.Information(1)
		return result

	def get_para_no_for_end_of_selection(self):
		""" 선택영역의 끝 문단 번호 """
		start_para = self.get_para_no_for_start_of_selection()
		len_para = self.selection.Range.ComputeStatistics(4)
		return start_para + len_para - 1

	def get_para_no_for_start_of_selection(self):
		""" 선택영역의 시작 문단 번호 """
		x = self.word_application.Selection.Start
		y = self.word_application.Selection.End
		new_range = self.doc.Range(Start=0, End=y)

		result = new_range.Paragraphs.Count
		return result

	def get_para_object_all_for_doc(self):
		"""
		현재 화성화된 문서 모든 문단객체를 돌려준다
		형태적인 분류 : active_doc(화일) > sentence(문장) > word(한 단어) > character(한글자)
		의미적인 분류 : active_doc(화일) > paragraph(문단) > line(줄) > word(한 단어) > character(한글자)
		sentence : 표현이 완결된 단위, 그 자체로 하나의 서술된 문장이 되는 것
		paragraph : 줄바꿈이 이루어지기 전까지의 자료

		"""
		result = self.doc.Paragraphs
		return result

	def get_range_object_for_nth_para_from_start_of_doc(self, input_para_no):
		result = self.doc.Paragraphs(input_para_no - 1).Range
		return result

	def get_range_object_for_selection(self):
		result = self.selection.Range
		return result

	def get_range_object_from_start_of_doc_to_nth_para(self, input_para_no):
		"""
		현재 화성화된 워드에서 문단번호로 문단객체를 갖고온다

		:param input_para_no: 문단번호
		"""
		result = self.doc.Paragraphs(input_para_no - 1)
		return result

	def get_size_for_table(self, input_table_obj):
		"""
		테이블객체의 가로세로의 크기
		:param input_table_obj:
		"""
		table_obj = self.check_table_object(input_table_obj)
		x_no = table_obj.Rows.Count
		y_no = table_obj.Columns.Count
		result = [x_no, y_no]
		return result

	def get_style_name_all(self):
		"""
		현재 화성화된 워드 화일안의 모든 스타일을 돌려준다
		"""
		result = []
		style_count = self.doc.Styles.Count
		for i in range(1, style_count + 1):
			style_object = self.doc.Styles(i)
			result.append(style_object.NameLocal)
		return result

	def get_table_no_all_in_selection(self):
		"""
		선택한 영역안의 테이블 번호들을 돌려준다
		"""
		result = []
		current_selection = self.selection.Range.Start
		for index, one in enumerate(self.doc.Tables):
			t_start = one.Range.Start
			t_end = one.Range.End
			if current_selection > t_start and current_selection < t_end:
				result.append(index + 1)
		return result

	def get_table_no_in_para_no(self, input_no):
		"""
		paragraph 번호에 따라서 그안에 테이블이 있으면, 테이블의 index 번호를 갖고온다

		:param input_no:
		"""
		result = None
		my_range = self.doc.Paragraphs(input_no + 1).Range
		try:
			if my_range.lnformation(12):
				tbl_index = self.count_table_in_selection()
				if tbl_index:
					# print("====> 테이블안에 있네요", tbl_index)
					result = tbl_index
		except:
			result = None
		return result

	def get_table_object_all(self):
		"""
		현재 화성화된 워드 화일안의 모든 테이블객체를 돌려준다
		테이블 객체란 테이블에대한 모든 정보를 갖고있는 클래스의 인스턴스이다
		"""
		self.all_table_obj = self.doc.Tables
		return self.all_table_obj

	def get_table_object_by_no(self, input_no):
		"""
		번호로 테이블객체를 갖고오는 것
		:param input_no:
		"""
		result = self.doc.Tables(input_no - 1)
		return result

	def get_text_all_in_doc(self):
		"""
		문서안의 모든 텍스트를 선택
		"""
		all_para_text = {}
		table_text = {}
		self.move_cursor_to_start_of_doc()
		para_nos = self.count_para_in_doc()
		for no in range(para_nos):
			self.select_from_start_of_doc_to_nth_letter_type("para", no)
			text_value = self.read_text_for_selection()
			# print("5# #& ==> ", no, text_value)
			all_para_text[no] = text_value
			try:
				ddd = self.selection.Information(12)
				# print(no, str(ddd))
				if ddd == True:
					zzz = self.count_table_in_selection()
			# print("테이블안에 있음", zzz)
			except:
				pass
		return para_nos

	def get_word_no_at_end_of_selection(self):
		"""
		선택영역의 끝단어 번호
		"""
		start_word = self.get_word_no_at_start_of_selection()
		len_word = self.selection.Range.ComputeStatistics(0)
		return start_word + len_word - 1

	def get_word_no_at_start_of_selection(self):
		"""
		선택영역의 시작 단어 번호
		"""
		x = self.word_application.Selection.Start
		y = self.word_application.Selection.End
		new_range = self.doc.Range(Start=0, End=x)

		result = new_range.Words.Count
		return result

	def get_xy_for_range(self):
		"""
		range안의 문단수
		"""
		#print(self.doc.Range)
		x = self.doc.Range.Start
		y = self.doc.Range.End
		return [x, y]

	def get_xy_for_selection(self):
		"""
		선택된 영역의 위치시작과 끝의 번호값을 갖고온다
		"""
		x = self.word_application.Selection.Start
		y = self.word_application.Selection.End
		return [x, y]

	def goto_range(self, input_range, letter_type, go_back="back", step=1):
		"""
		range 의 next 와 비슷한 효과이지만，
		range 에 없는 다양한 형 태로 가능하다
		예를들어 spelling error 이 발생하거나, 코멘트한곳등

		:param input_range:
		:param letter_type:
		:param go_back:
		:param step:
		:return:
		"""
		input_range.GoTo(letter_type, go_back, step)

	def goto_range_by_date(self, input_range, letter_type, go_back="back", step=1):
		input_range.GoTo(letter_type, go_back, step, "Date")

	def insert_new_para_with_properties(self, input_text, size=14, font="Arial", align="right", bold=True,
										input_color="red", style="표준"):
		"""
		선택한 위치에 글을 쓴다
		형태적인 분류 : active_doc(화일) > sentence(문장) > word(한 단어) > character(한글자)
		의미적인 분류 : active_doc(화일) > paragraph(문단) > line(줄) > word(한 단어) > character(한글자)
		sentence : 표현이 완결된 단위, 그 자체로 하나의 서술된 문장이 되는 것
		paragraph : 줄바꿈이 이루어지기 전까지의 자료


		wdAlignParagraphCenter	1	Center-aligned.
		wdAlignParagraphJustify	3	Fully justified.
		wdAlignParagraphLeft	0	Left-aligned.
		wdAlignParagraphRight	2	Right-aligned.

		:param input_text:
		:param size:
		:param font:
		:param align:
		:param bold:
		:param input_color:
		:param style:
		"""

		temp_value = self.color.change_scolor_to_rgb(input_color)
		rgb_int = self.color.change_rgb_to_rgbint(temp_value)

		self.word_application.Selection.InsertAfter(input_text + "\r\n")
		para_no = self.get_para_no_for_start_of_selection()
		self.select_from_start_of_doc_to_nth_letter_type("para", para_no)

		self.selection.Style = style
		self.selection.Range.Font.Name = font
		self.selection.Range.Font.Bold = bold
		self.selection.Range.Font.Size = size
		self.selection.Font.TextColor.RGB = rgb_int
		self.doc.Paragraphs(para_no - 1).Alignment = 2

	def information_for_doc(self):
		# 현재 문서의 기본적인 정보들을 알려줍니다
		result = {}

		file_name = self.get_active_doc_name()
		para_no = self.count_para_in_doc()
		word_no = self.count_word_in_doc()
		char_no = self.count_char_in_doc()
		result["file_name"] = file_name
		result["para_no"] = para_no
		result["word_no"] = word_no
		result["char_no"] = char_no
		return result

	def information_for_range(self, input_range):
		x = input_range.Start
		y = input_range.End
		self.doc.Range(Start=x, End=y).Select()
		result = self.information_for_selection()
		return result

	def information_for_selection(self):
		"""
		현재 선택된 자료의 정보를 알려준다

		"""
		result = {}
		len_char = self.selection.Range.ComputeStatistics(3)
		result["len_char"] = len_char
		len_word = self.selection.Range.ComputeStatistics(0)
		result["len_word"] = len_word
		len_line = self.selection.Range.ComputeStatistics(1)
		result["len_line"] = len_line
		len_para = self.selection.Range.ComputeStatistics(4)
		result["len_para"] = len_para
		len_page = self.selection.Range.ComputeStatistics(2)
		result["len_page"] = len_page

		start_word_no = self.get_char_no_for_start_of_selection()
		result["start_word_no"] = start_word_no

		print("selection : 시작 페이지 번호 => ", self.selection.Information(1))
		result["start_page_no"] = self.selection.Information(1)

		print("selection : 끝 페이지 번호 => ", self.selection.Information(3))
		result["end_page_no"] = self.selection.Information(3)

		print("selection : 끝 섹션 번호 => ", self.selection.Information(2))
		result["end_section_no"] = self.selection.Information(2)

		print("selection : 테이블안의 자료인지 => ", self.selection.Information(12))
		result["is_in_table"] = self.selection.Information(12)

		print("selection : 테이블에서 처음것의 y번호 => ", self.selection.Information(16))
		result["start_y_no_in_table"] = self.selection.Information(16)

		print("selection : 테이블에서 처음것의 x번호 => ", self.selection.Information(13))
		result["start_x_no_in_table"] = self.selection.Information(13)

		print("selection : 테이블에서 마지막것의 y번호 => ", self.selection.Information(14))
		result["end_y_no_in_table"] = self.selection.Information(14)

		print("selection : 테이블에서 마지막것의 x번호 => ", self.selection.Information(17))
		result["end_x_no_in_table"] = self.selection.Information(17)

		print("selection : 라인의 처음에서 첫번째 문자의 시작 번호 => ", self.selection.Information(9))
		result["start_char_no_in_line"] = self.selection.Information(9)

		print("selection : 첫번째 문자의 라인번호 => ", self.selection.Information(10))
		result["start_line_no"] = self.selection.Information(10)

		print("selection : 테이블에서 최대가능 x줄수 => ", self.selection.Information(18))
		result["max_table_x_no"] = self.selection.Information(18)

		print("selection : 테이블에서 최대가능 y줄수 => ", self.selection.Information(15))
		result["max_table_y_no"] = self.selection.Information(15)

		print("selection : 최대가능 페이지수 => ", self.selection.Information(4))
		result["total_page_no"] = self.selection.Information(4)

		print("selection : 선택된 문자 => ", self.word_application.Selection.Text)
		result["text"] = self.word_application.Selection.Text

		return result

	def insert_new_line_at_end_of_selection(self):
		self.selection.InsertBefore("\r\n")

	def insert_no_colored_table_for_selection(self, x_no, y_no):
		"""
		커서위치에 테이블삽입
		단, 선의 색이 없는 것을 적용해서 문서를 넣어서 사용하는 것을 만드는 것이다

		:param x_no:
		:param y_no:
		"""
		self.table_obj = self.doc.Tables.Add(self.selection.Range, x_no, y_no)
		self.table_obj.Borders.LineStyle = 0  # wdLineStyleNone =0
		return self.table_obj

	def insert_one_xline_at_end_of_table(self, table_obj):
		"""
		테이블에 가로행을 추가하는것 (아랫부분에 추가)

		:param table_obj:  테이블 객제
		"""
		total_row = table_obj.Rows.Count
		table_obj.Rows(total_row).Select()
		self.selection.InsertRowsBelow(1)

	def insert_picture_at_cursor(self, file_full_name, size_w, size_h):
		"""
		커서위치에 그림삽입

		:param file_full_name:
		:param size_w:
		:param size_h:
		:return:
		"""
		current_pic = self.word_application.Selection.range.InlineShapes.AddPicture(file_full_name)
		current_pic.Height = size_h
		current_pic.Width = size_w

	def insert_picture_for_selection(self, file_full_name, size_w, size_h):
		"""
		커서위치에 그림삽입

		:param file_full_name:
		:param size_w:
		:param size_h:
		"""
		current_pic = self.word_application.Selection.range.InlineShapes.AddPicture(file_full_name)
		current_pic.Height = size_h
		current_pic.Width = size_w

	def insert_picture_in_table_by_xy(self, table_obj, xy, file_full_name, padding=1):
		# 테이블의 크기게 맞도록 사진을 넣기
		if type(table_obj) == type(1):
			table_obj = self.doc.Tables(table_obj)
		range_obj = table_obj.Cell(Row=xy[0], Column=xy[1]).Range
		cell_w = table_obj.Cell(Row=xy[0], Column=xy[1]).Width - padding
		cell_h = table_obj.Cell(Row=xy[0], Column=xy[1]).Height - padding
		picture_obj = range_obj.InlineShapes.AddPicture(file_full_name)
		picture_obj.Width = cell_w
		picture_obj.Height = cell_h

	def insert_table_at_cursor(self, x_no, y_no):
		"""
		커서위치에 테이블삽입

		:param x_no:
		:param y_no:
		:return:
		"""
		table_obj = self.doc.Tables.Add(self.selection.Range, x_no, y_no)
		self.draw_line_style_for_table(table_obj)
		return table_obj

	def insert_table_at_end_of_para(self, para_no, table_xy=[5, 5]):
		"""
		없애도 되는 것
		선택한 문단뒤에 테이블을 만든다
		형태적인 분류 - active_doc(화일) > sentence(문장) > word(한 단어) > character(한글자)
		의미적인 분류 - active_doc(화일) > paragraph(문단) > line(줄) > word(한 단어) > character(한글자)
		sentence - 표현이 완결된 단위, 그 자체로 하나의 서술된 문장이 되는 것
		paragraph - 줄바꿈이 이루어지기 전까지의 자료

		:param para_no:
		:param table_xy:
		"""
		myrange = self.doc.Paragraphs(para_no).Range
		mytable = self.doc.Tables.Add(myrange, table_xy[0], table_xy[1])
		mytable.AutoFormat(36)

	def insert_xxline_in_table(self, table_obj, xx):
		"""
		테이블객체의 테이블에 가로행을 추가하는 것 (아랫부분에 추가)

		:param table_obj:  테이블 객제
		:param xx: 가로행의 시작 번호
		"""
		table_obj.Rows(xx[0]).Select()
		self.selection.InsertRowsBelow(xx[1] - xx[0])

	def insert_yyline_in_table(self, table_obj, yy):
		"""
		테이블객체의 테이블에 세로행을 추가하는 것 (오른쪽에 추가)

		:param table_obj:  테이블 객제
		:param yy: 세로행의 시작 번호
		"""
		table_obj.Columns(yy[0]).Select()
		self.selection.InsertColumnsRight(yy[1] - yy[0])

	def is_scolor_style(self, input_scolor):
		"""
		scolor용
		입력된 자료의 형태가, scolor형식인지를 확인하는 것
		"""
		result1 = self.jf.search_all_by_jf_sql("[한글&영어:2~10][숫자:0~7]", str(input_scolor))
		result2 = self.jf.search_all_by_jf_sql("[한글&영어:2~10][+-:0~7]", str(input_scolor))

		if result1 and result2:
			result = result1[0]
		elif result1 and not result2:
			result = result1[0]
		elif not result1 and result2:
			result = result2[0]
		elif not result1 and not result2:
			result = False
		return result

	def make_table_obj_with_black_line(self, row_line_no=3, col_line_no=3):
		"""

		:param row_line_no:
		:param col_line_no:
		:return:
		"""
		new_table_obg = self.doc.Tables.Add(Range=self.selection.Range, NumRows=row_line_no,
		                                             NumColumns=col_line_no, DefaultTableBehavior=0, AutoFitBehavior=0)
		new_table_obg.Cell(1, 3).range.ParagraphFormat.Alignment = 0
		for no in [-1, -2, -3, -4, -5, -6]:
			new_table_obg.Borders(no).LineStyle = 1
		new_table_obg.Rows.Height = 10
		return new_table_obg

	def merge_entire_xline_at_table_obj(self, table_obj, start_x):
		"""
		선택된 가로줄을 전부 병합시키는것

		:param table_obj:  테이블 객제
		:param start_x: 가로줄번호
		"""
		count_y = table_obj.Columns.Count
		count_x = table_obj.Rows.Count
		# print(count_x, count_y)
		table_obj.Cell(start_x, 1).Merge(MergeTo=table_obj.Cell(start_x, count_y))

	def merge_entire_yline_at_table_obj(self, table_obj, start_y):
		"""
		선택된 세로줄을 전부 병합시키는것

		:param table_obj:  테이블 객제
		:param start_y: 세로줄번호
		"""
		count_y = table_obj.Columns.Count
		count_x = table_obj.Rows.Count
		# print(count_x, count_y)
		table_obj.Cell(1, start_y).Merge(MergeTo=table_obj.Cell(count_x, start_y))

	def merge_xyxy_in_table_obj(self, table_obj, xyxy):
		"""
		테이블의 가로와 세로번호까지의 영역을 병합

		:param table_obj:  테이블 객제
		:param xyxy: [가로시작, 세로시작, 가로끝, 세로끝]
		"""
		my_range = self.doc.Range(Start=table_obj.Cell(xyxy[0], xyxy[1]).Start,
								  End=table_obj.Cell(xyxy[2], xyxy[3]).End)
		my_range.Select()
		self.selection.Cells.Merge()

	def move_cursor_from_start_of_doc_to_nth_char(self, input_no):
		self.move_cursor_to_start_of_doc()
		self.move_cursor_to_nth_letter_type_from_selection("char", input_no-1)

	def move_cursor_to_begin_of_doc(self):
		"""
		활성화된 워드화일의 처음으로 커서를 이동

		:return:
		"""
		self.selection.HomeKey(Unit=6)

	def move_cursor_to_end_of_doc(self):
		"""
		문서의 끝으로 커서를 이동
		맨마지막에 글자를 추가하거나 할때 사용한다
		"""
		self.selection.EndKey(Unit=6)

	def move_cursor_to_end_of_selection(self):
		"""
		선택영역의 끝으로 커서를 이동
		"""
		y = self.selection.Range.End
		self.doc.Range(y, y).Select()
		return self.selection

	def move_cursor_to_end_of_selection_rev1(self):
		"""
		현재 선택영역의 끝으로 커서가 이동
		"""
		self.word_application.Selection.EndOf()

	def move_cursor_to_nth_char_from_selection(self, input_no):
		self.move_cursor_to_nth_letter_type_from_selection("char", input_no)

	def move_cursor_to_nth_char_from_start_of_doc(self, input_no):
		self.move_cursor_to_nth_letter_type_from_start_of_doc("char", input_no)

	def move_cursor_to_nth_letter_type_from_selection(self, letter_type, input_no):
		"""
		가능한 형식
		movedown이 되는 것
		"cell" = 12, "character" = 1, "char" = 1, "column" = 9
		"item" = 16, "line" = 5, "paragraph" = 4, "para" = 4
		"row" = 10, "section" = 8, "sentence" = 3, "story" = 6
		"table" = 15, "word" = 2
		"""
		letter_type_no = self.check_letter_type_no(letter_type)
		if input_no > 0:
			if letter_type_no in [3, 2, 1]:
				self.selection.MoveRight(Unit=letter_type_no, Count=input_no)
			else:
				self.selection.MoveDown(Unit=letter_type_no, Count=input_no)
		else:
			if letter_type_no in [3, 2, 1]:
				self.selection.MoveLeft(Unit=letter_type_no, Count=input_no)
			else:
				self.selection.MoveUp(Unit=letter_type_no, Count=input_no)

	def move_cursor_to_nth_letter_type_from_start_of_doc(self, letter_type, input_no):
		self.move_cursor_to_start_of_doc()

		letter_type_no = self.check_letter_type_no(letter_type)

		if input_no > 0:
			if letter_type_no in [3, 2, 1]:
				self.selection.MoveRight(Unit=letter_type_no, Count=input_no)
			else:
				self.selection.MoveDown(Unit=letter_type_no, Count=input_no)
		else:
			if letter_type_no in [3, 2, 1]:
				self.selection.MoveLeft(Unit=letter_type_no, Count=input_no)
			else:
				self.selection.MoveUp(Unit=letter_type_no, Count=input_no)

	def move_cursor_to_nth_line_from_selection(self, input_no):
		self.move_cursor_to_nth_letter_type_from_selection("line", input_no)

	def move_cursor_to_nth_line_from_start_of_doc(self, input_no):
		""" 현재커서를 문서의 처음에서부터 n번째 라인의 맨앞으로 이동"""
		self.move_cursor_to_nth_letter_type_from_start_of_doc("line", input_no-1)

	def move_cursor_to_nth_para_from_selection(self, input_no):
		self.move_cursor_to_nth_letter_type_from_selection("para", input_no)

	def move_cursor_to_nth_para_from_start_of_doc(self, input_no):
		""" 현재커서를 문서의 처음에서부터 n번째 문단의 맨앞으로 이동"""
		self.move_cursor_to_nth_letter_type_from_start_of_doc("para", input_no-1)

	def move_cursor_to_nth_sentence_from_selection(self, input_no):
		self.move_cursor_to_nth_letter_type_from_selection("sentence", input_no)

	def move_cursor_to_nth_word_from_selection(self, input_no):
		self.move_cursor_to_nth_letter_type_from_selection("word", input_no)

		#self.selection.GoTo(What=2, Which=(lambda x: 2 if (x > 0) else 3)(input_no), Count=abs(input_no))

	def move_cursor_to_nth_word_from_start_of_doc(self, input_no):
		""" 현재커서를 문서의 처음에서부터 n번째 워드의 맨앞으로 이동"""
		self.move_cursor_to_nth_letter_type_from_start_of_doc("word", input_no)

	def move_cursor_to_start_of_doc(self):
		"""
		활성화된 워드화일의 처음으로 커서를 이동
		"""
		#print("==> ", self.selection.Start)
		self.doc.Range(0, 0).Select()

	def move_cursor_to_start_of_selection(self):
		"""
		selection의 영역을 없애고, 영역의 시작위치로 커서만 남기는것
		"""
		self.selection.range.Collapse()
		return self.selection

	def move_cursor_with_option(self, para=0, line=0, word=0, char=0):
		"""
		현재 커서에서 원하는 곳으로 이동을 하는 것

		+ : 뒤로 이동
		- : 앞으로 이동
		0 : 그자리
		end : 끝으로
		start, start : 시작

		what : 3(라인), 1(페이지), 0(섹션), 2(테이블), 9(객체)
		Which : 1(처음), -1(끝),2(다음객체로), 3(전객체로)
		"""

		if para != 0: self.selection.GoTo(What=4, Which=(lambda x: 2 if (x > 0) else 3)(para), Count=abs(para))
		if line != 0: self.selection.GoTo(What=3, Which=(lambda x: 2 if (x > 0) else 3)(line), Count=abs(line))
		if word != 0: self.selection.GoTo(What=2, Which=(lambda x: 2 if (x > 0) else 3)(word), Count=abs(word))
		if char != 0: self.selection.GoTo(What=1, Which=(lambda x: 2 if (x > 0) else 3)(char), Count=abs(char))

		return self.selection

	def move_range_to_nth_letter_type(self, input_range, letter_type, input_no):
		"""
		현재 range영역 + 입력형태의 끝까지 영역을 확장 하는 것

		현재 위치에서 원하는 문자의 형태 끝까지 영역을 확대 하는 것
		move : range객체의 start를 이동시키는 것,

		letter_type : 어떻게 이동을 하는지를 설정하는 것입니다
		input_no : +는 뒤로, -는 앞으로 이동한다
		"""

		# 기존의 자료를 저장한다

		if input_range=="":
			input_range = self.word_application.Selection

		old_x = input_range.Start
		old_y = input_range.End
		letter_type_no = self.vars["word"]["letter_type"][letter_type]

		if letter_type in ["char", "word", "line", "para"]:
			# 어떤 형태라도 range의 끝점을 이동시키는 것
			if input_no > 0:
				input_range.Move(letter_type_no, input_no)
				new_x1 = input_range.Start
				input_range.Move(letter_type_no, 1)
				new_x2 = input_range.Start
				# print("--> ", new_x1, new_x2)
				new_range_object = self.doc.Range(old_x, new_x2)
			else:
				input_range.Move(letter_type_no, input_no)
				new_x1 = input_range.Start
				input_range.Move(letter_type_no, -1)
				new_x2 = input_range.Start
				# print("값이 음수일때 --> ", old_x, old_y, new_x1, new_x2)
				new_range_object = self.doc.Range(min(new_x1, new_x2), max(old_x, old_y))
		return new_range_object

	def new_doc(self):
		"""		새 문서를		"""
		self.word_application.Documents.Add()

	def new_doc_for_range(self, x, y, new_doc_name=""):
		# a 워드화일의 일정부분을 새로운 워드를 열어서 저장하는 것
		input_range = self.doc.Range(x, y)
		input_range.Copy()
		self.__check_doc("new")
		self.selection.FormattedText = input_range
		self.save_as(new_doc_name)

	def new_range_by_xy(self, xy):
		# 그냥 range 라는 단어를 썼다가，파이썬의 예약어와 충돌을 일으켰다
		new_range = self.doc.Range(xy[0] - 1, xy[1])
		return new_range

	def new_table(self, row_line_no=3, col_line_no=3):
		"""
		기본적인 형태의 테이블 객체를 만든다

		:param row_line_no:
		:param col_line_no:
		"""

		new_table_obg = self.doc.Tables.Add(Range=self.selection.Range, NumRows=row_line_no,
											NumColumns=col_line_no,
											DefaultTableBehavior=0, AutoFitBehavior=0)
		new_table_obg.Cell(1, 3).range.ParagraphFormat.Alignment = 0

		return new_table_obg

	def new_table_with_black_line(self, row_line_no=3, col_line_no=3):
		"""

		:param row_line_no:
		:param col_line_no:
		"""
		new_table_obg = self.doc.Tables.Add(Range=self.selection.Range, NumRows=row_line_no,
											NumColumns=col_line_no, DefaultTableBehavior=0,
											AutoFitBehavior=0)
		new_table_obg.Cell(1, 3).range.ParagraphFormat.Alignment = 0
		for no in [-1, -2, -3, -4, -5, -6]:
			new_table_obg.Borders(no).LineStyle = 1
		new_table_obg.Rows.Height = 10
		return new_table_obg

	def paint_background_color_for_selection(self, input_color):
		"""
		선택된 영역의 배경색을 지정하는것

		:param input_color:
		"""
		rgb = self.color.change_scolor_to_rgb(input_color)
		rgb_int = self.color.change_rgb_to_rgbint(rgb)
		self.selection.Range.Shading.BackgroundPatternColor = rgb_int

	def paint_background_color_in_selection(self, input_color):
		"""
		선택된 영역의 배경색을 지정하는것

		:param input_color:
		:return:
		"""

		rgb = self.color.change_scolor_to_rgb(input_color)
		rgb_int = self.color.change_rgb_to_rgbint(rgb)
		self.selection.Range.Shading.BackgroundPatternColor = rgb_int

	def paint_backgroundcolor_for_selection(self):
		"""
		배경색넣기
		#	16764057	wdColorPaleBlue	Pale blue color
		#	16711935	wdColorPink	Pink color
		#	6697881	wdColorPlum	Plum color
		#	255	wdColorRed	Red color
		#	13408767	wdColorRose	Rose color
		#	6723891	wdColorSeaGreen	Sea green color
		#	16763904	wdColorSkyBlue	Sky blue color
		#	10079487	wdColorTan	Tan color
		#	8421376	wdColorTeal	Teal color
		#	16776960	wdColorTurquoise	Turquoise color
		#	8388736	wdColorViolet	Violet color
		#	16777215	wdColorWhite	White color
		#	65535	wdColorYellow	Yellow color
		"""

		self.selection.Font.Shading.ForegroundPatternColor = 255
		self.selection.Font.Shading.BackgroundPatternColor = 255

	def paint_border_for_selection(self, input_color):
		"""
		:param input_color:
		"""
		rgbint = self.color.change_scolor_to_rgbint(input_color)

		self.selection.Font.Borders(1).LineStyle = 1
		self.selection.Font.Borders(1).Color = rgbint

	def paint_border_for_selection_no_line(self, input_color):
		"""
		선택영역의 외곽선을 그리기

		:param input_color: 색이름
		"""
		self.selection.Font.Borders.Color = self.color.change_scolor_to_rgbint(input_color)

	def paint_border_in_selection(self, input_color):
		"""

		:param input_color:
		:return:
		"""
		self.selection.Font.Borders(1).LineStyle = 1
		self.selection.Font.Borders(1).Color = self.vars["ganada"]["color_24bit"][input_color]

	def paint_color_for_cell_in_table(self, table_obj, xy, color_index="red"):
		"""
		테이블객체의 가로세로번호의 셀의 배경색을 색칠하기

		:param table_obj:  테이블 객제
		:param xy:
		:param color_index:
		"""
		table_obj.Cell(xy[0], xy[1]).Shading.BackgroundPatternColor = self.vars["word"]["color_24bit"][color_index]

	def paint_highlight_for_selection(self, input_color):
		"""
		선택영역의 글자들의 배경을 하이라이트를 설정

		:param input_color: 색이름
		"""
		self.selection.Range.HighlightColorIndex = self.vars["word"]["color_index"][input_color]

	def paint_highlight_from_char_no1_to_char_no2(self, input_no1, input_no2, input_color="blu"):
		"""
		선택영역의 글자들의 배경을 하이라이트를 설정

		:param input_color: 색이름
		"""
		my_range = self.doc.Range(Start=input_no1, End=input_no2)
		my_range.HighlightColorIndex = self.vars["word"]["color_index"][input_color]

	def paint_selection(self, input_color):
		self.paint_background_color_for_selection(input_color)

	def paint_shading_background_for_selection(self, input_color):
		"""
		선택영역의 배경색의 음영설정

		:param input_color: 색이름
		"""
		self.selection.Font.Shading.BackgroundPatternColor = self.vars["word"]["color_24bit"][input_color]

	def paint_shading_foreground_for_selection(self, input_color):
		"""
		선택영역의 foreground의 음영설정

		:param input_color: 색이름
		"""
		self.selection.Font.Shading.ForegroundPatternColor = self.vars["word"]["color_24bit"][input_color]

	def paste_selection(self):
		"""
		선택영역에 붙여넣기
		"""
		self.word_application.Selection.Paste()

	def print_as_pdf(self, file_name):
		"""
		pdf로 저장

		:param file_name:
		"""
		self.doc.ExportAsFixedFormat(OutputFileName=file_name, ExportFormat=17),

	def quit(self):
		"""
		워드 프로그램 종료
		"""
		self.word_application.Quit()

	def read_all_text_for_selection(self):
		x_no = self.word_application.Selection.Start
		y_no = self.word_application.Selection.End
		temp = self.doc.Range(x_no, y_no).Text
		result = temp.split(chr(13))
		all_text = ""
		for one in result:
			all_text = all_text + one
		return all_text

	def read_all_text_in_doc(self):
		"""
		현재 문서에서 모든 텍스트만 돌려준다
		"""
		result = self.doc.Range().Text
		return result

	def read_table_as_list_2d(self, table_no=1):
		"""
		테이블의 모든 값을 2차원 리스트형태의 값으로 읽어오는것

		:param table_no:
		"""

		result = []
		table = self.doc.Tables(table_no)
		table_x_no = table.Rows.Count
		table_y_no = table.Columns.Count
		for x in range(1, table_x_no + 1):
			temp_line = []
			for y in range(1, table_y_no + 1):
				aaa = table.Cell(Row=x, Column=y).Range.Text
				temp_line.append(str(aaa).replace("\r\x07", ""))
			result.append(temp_line)
		return result

	def read_table_index_by_paragraph_index(self, input_no):
		"""
		아래의 것은 잘못된 부분이 있어서, 변경을 하였다
		paragraph번호에 따라서 그안에 테이블이 있으면, 테이블의 index번호를 갖고온다

		:param input_no:
		"""
		result = None
		my_range = self.doc.Paragraphs(input_no + 1).Range
		try:
			if my_range.Information(12):
				tbl_index = self.count_table_in_selection()
				if tbl_index:
					# print("====>  테이블안에 있네요", tbl_index)
					result = tbl_index
		except:
			result = None
		return result

	def read_text_between_para_1_to_para_2(self, para1_index, para2_index):
		"""
		선택한 2개의 문단 번호 사이의 글을 돌려준다

		:param para1_index:
		:param para2_index:
		"""
		start = self.doc.Paragraphs(para1_index).Range.Start
		end = self.doc.Paragraphs(para2_index).Range.End
		result = self.doc.Range(start, end).Text
		return result

	def read_text_for_current_char(self, input_no=1):
		"""
		현재 커서가 있는 문단을 선택해서, 그 문단 전체의 text를 돌려준다
		형태적인 분류 : active_doc(화일) > sentence(문장) > word(한 단어) > character(한글자)
		의미적인 분류 : active_doc(화일) > paragraph(문단) > line(줄) > word(한 단어) > character(한글자)
		sentence : 표현이 완결된 단위, 그 자체로 하나의 서술된 문장이 되는 것
		paragraph : 줄바꿈이 이루어지기 전까지의 자료

		:param input_no: 번호
		"""
		#self.expand_selection_to_nth_char(input_no)
		return self.word_application.Selection.Text

	def read_text_for_current_line(self, input_no=1):
		"""
		:param input_no: 번호
		"""
		result = self.get_line_at_cursor()
		return result

	def read_text_for_current_para(self, input_no=1):
		"""
		현재 커서가 있는 문단을 선택해서, 그 문단 전체의 text를 돌려준다
		형태적인 분류 : active_doc(화일) > sentence(문장) > word(한 단어) > character(한글자)
		의미적인 분류 : active_doc(화일) > paragraph(문단) > line(줄) > word(한 단어) > character(한글자)
		sentence : 표현이 완결된 단위, 그 자체로 하나의 서술된 문장이 되는 것
		paragraph : 줄바꿈이 이루어지기 전까지의 자료

		:param input_no: 번호
		"""
		self.selection.GoTo(What=4, Which=1, Count=input_no)
		result = self.word_application.Selection.range.Text
		return result

	def read_text_for_current_range(self):
		"""
		range영역의 text를 갖고온다
		"""
		result = self.doc.Range().Text
		return result

	def read_text_for_current_word(self):
		myRange = self.word_application.Words(1)
		result = myRange.Text
		return result

	def read_text_for_next_line_from_cursor(self):
		"""
		현재 커서가 있는 라인의 다음줄을 뜻한다
		커서의 위치는 커서가 시작하는 위치이다
		"""
		start_line_no_at_cursor = self.selection.Information(10)
		self.select_nth_line_from_start_of_doc(start_line_no_at_cursor+1)
		self.expand_selection_to_nth_line(1)
		return self.word_application.Selection.Text

	def read_text_for_nth_char_from_start_of_doc(self, input_no):
		"""
		문서의 처음에서부터 n번째 글자를 선택하는 방법
		"""
		self.select_nth_char_from_start_of_doc(input_no)
		self.expand_selection_to_nth_char(1)
		return self.word_application.Selection.Text

	def read_text_for_nth_line_from_cursor(self, input_no):
		"""
		현재 커서가 있는 라인의 다음줄을 뜻한다
		커서의 위치는 커서가 시작하는 위치이다
		"""
		start_line_no_at_cursor = self.selection.Information(10)
		self.select_nth_line_from_start_of_doc(start_line_no_at_cursor+1)
		self.select_nth_line_from_selection(input_no)
		return self.word_application.Selection.Text

	def read_text_for_nth_line_from_start_of_doc(self, input_no):
		"""
		문서의 처음에서부터 n번째 라인을 선택하는 방법
		"""
		self.select_nth_line_from_start_of_doc(input_no)
		self.expand_selection_to_nth_line(1)
		return self.word_application.Selection.Text

	def read_text_for_nth_para_from_start_of_doc(self, input_no):
		""" 문서의 처음에서부타 n번째의 단어를 갖고오는 것 """
		new_range = self.doc.Range(Start=0, End=len(self.doc.Characters))
		result = new_range.Paragraphs(input_no)
		return result

	def read_text_for_nth_word_from_start_of_doc(self, input_no):
		""" 문서의 처음에서부타 n번째의 단어를 갖고오는 것 """
		new_range = self.doc.Range(Start=0, End=len(self.doc.Characters))
		result = new_range.Words(input_no)
		return result

	def read_text_for_para_no(self, input_no):
		"""
		paragraph 번호에 따라서 해당하는 paragraph의 text 를 갖고오는것
		형태적인 분류 - active_doc(화일) > sentence(문장) > word(한 단어) > character(한글자)
		의미적인 분류 - active_doc(화일) > paragraph(문단) > line(줄) > word(한 단어) > character(한글자)
		sentence - 표현이 완결된 단위, 그 자체로 하나의 서술된 문장이 되는 것
		paragraph - 줄바꿈이 이루어지기 전까지의 자료

		:param input_no:
		"""
		aaa = self.doc.Paragraphs(input_no)
		result = aaa.Range.Text
		return result

	def read_text_for_range(self):
		"""
		range가 있으면, 그것을 없으면 selection의 값을 갖고온다

		:param input_range_object:
		"""
		if self.range:
			text = self.range.Text
		else:
			text = self.selection.Text

		return text

	def read_text_for_selection(self):
		rng_obj = self.word_application.Selection
		return rng_obj.Text

	def read_text_for_selection_as_list(self):
		x_no = self.word_application.Selection.Start
		y_no = self.word_application.Selection.End
		temp = self.doc.Range(x_no, y_no).Text
		result = temp.split(chr(13))
		return result

	def read_text_from_selection_to_nth_char(self):
		rng_obj = self.word_application.Selection
		return rng_obj.Text

	def read_text_from_start_of_para_by_len(self, input_index, x, length):
		"""
		선택된 문단에서 몇번째의 글을 선택하는 것
		일정 영역의 자료를 갖고오는 3
		paragraph를 선택한다, 없으면 맨처음부터
		형태적인 분류 - active_doc(화일) > sentence(문장) > word(한 단어) > character(한글자)
		의미적인 분류 - active_doc(화일) > paragraph(문단) > line(줄) > word(한 단어) > character(한글자)
		sentence - 표현이 완결된 단위, 그 자체로 하나의 서술된 문장이 되는 것
		paragraph - 줄바꿈이 이루어지기 전까지의 자료

		:param input_index:
		:param x:
		:param length:
		"""
		paragraph = self.doc.Paragraphs(input_index)
		# 맨앞에서 몇번째부터, 얼마의 길이를 선택할지를 선정
		x_no = paragraph.Range.Start + x - 1
		y_no = paragraph.Range.Start + x + length - 1
		result = self.doc.Range(x_no, y_no).Text
		return result

	def read_text_from_x_to_y(self, index_1, index_2):
		"""
		활성화된 워드화일의 문자번호 사이의 글자를 갖고온다

		:param index_1:
		:param index_2:
		"""
		result = self.doc.Range(index_1, index_2).Text
		return result

	def read_text_from_xy(self, x, y):
		"""
		활성화된 워드화일의 문자번호 사이의 글자를 갖고온다
		화일의 글자수를 기준으로 text를 읽어오는 것

		:param x:
		:param y:
		"""
		result = self.doc.Range(x, y).Text

	def read_text_in_table_by_xy(self, table_index, lxly):
		"""
		테이블객체에서 가로세로번호의 셀의 text값을 갖고온다

		:param table_index:
		:param lxly:
		"""
		table = self.doc.Tables(table_index)
		result = table.Cell(Row=lxly[0], Column=lxly[1]).Range.Text
		# str문자들은 맨 마지막에 끝이라는 문자가 자동으로 들어가서, 이것을 없애야 표현이 잘된다
		return result[:-1]

	def regex_for_selection(self, jf_sql):
		text_value = self.read_text_for_selection()
		result = self.jf.search_all_with_jf_sql(jf_sql, text_value)
		return result

	def release_selection(self, start_or_end=0):
		"""
		커서를 selection의 맨 끝을 기준으로 옮겨서 해제한것
		만약 선택영역에서 선택부분을 없애면서，커서를 기존 선택부분의 제일 앞으로 하려면 1을
		맨끝의 다음번 문자로 이동하려면，0을 넣는다
		예 : 12345678 중 345 가 선택되엇다면, 0 -> 6 앞에, 1 은 1 앞으로 커서이동
		"""
		self.selection.Collapse(start_or_end)

	def repalce_selection_text_to_input_text(self, input_text):
		"""
		선택되어진 영역의 값을 변경
		:param input_text: 바꿀 문자
		"""
		self.selection.Range.Text = input_text

	def replace_all(self, before_text, after_text):
		"""
		워드화일에서 한번에 원하는 글자를 바꾸는 것

		:param before_text: 찾을 문자
		:param after_text: 바꿀 문자
		:return:
		"""
		# aaa.Find.Execute(찾을단어, False, False, False, False, False, 앞쪽으로검색, 1, True, 바꿀문자, 전체변경/Replace)
		aaa = self.doc.Range(Start=0, End=self.doc.Characters.Count)
		aaa.Find.Execute(before_text, False, False, False, False, False, True, 1, True, after_text, 2)

	def replace_all_in_doc_with_colored(self, search_text, replace_text, color_name="red"):
		"""
		화일안의 모든 문자를 바꾸고 색칠하기

		:param search_text:
		:param replace_text:
		:param color_name:
		"""

		self.release_selection()
		# 이것이 없으면, 커서이후부터 찾는다
		self.move_cursor_to_start_of_doc()
		result = []
		temp_value = self.color.change_scolor_to_rgb(color_name)
		rgb_int = self.color.change_rgb_to_rgbint(temp_value)

		while self.selection.Find.Execute(search_text):
			self.selection.Range.Font.Italic = True
			self.selection.Range.Font.TextColor.RGB = rgb_int
			self.selection.Range.HighlightColorIndex = 7  # 7번은 노랑, 6번은 빨강

			start_no = self.selection.Range.Start
			end_no = start_no + len(search_text)
			self.selection.Range.Text = replace_text

	def replace_all_with_color_from_selection_to_end(self, search_text, replace_text, color_name="red"):
		"""
		현재위치 이후의 모든것을 변경
		"""
		self.release_selection()
		# 이것이 없으면, 커서이후부터 찾는다
		# self.move_cursor_to_start_of_doc()
		result = []
		temp_value = self.color.change_scolor_to_rgb(color_name)
		rgb_int = self.color.change_rgb_to_rgbint(temp_value)

		while self.selection.Find.Execute(search_text):
			self.selection.Range.Font.Italic = True
			self.selection.Range.Font.TextColor.RGB = rgb_int
			self.selection.Range.HighlightColorIndex = 7  # 7번은 노랑, 6번은 빨강

			start_no = self.selection.Range.Start
			end_no = start_no + len(search_text)
			self.selection.Range.Text = replace_text

	def replace_in_doc_by_jfsql(self, jfsql="", replace_text=""):
		"""
		jf_sql로 문서안의 모든 글자를 변경

		:param jfsql:
		:param replace_text:
		"""
		para_nos = self.count_para_in_doc()
		for index in range(para_nos):
			my_range = self.doc.Paragraphs(index + 1).Range
			my_range_text = my_range.Text
			# print(index, my_range_text)
			regex_result = self.jf.search_all_by_jf_sql(jfsql, my_range.Text)
			# print(regex_result)
			if regex_result:
				for list_1d in regex_result:
					# self.replace_one_time_from_selection(regex_result[0][0], replace_text)

					my_range.Find.Execute(list_1d[0], False, False, False, False, False, True, 1, True, replace_text, 2)

	def replace_one_time_from_selection(self, search_text, replace_text):
		"""
		전체가 아니고 제일 처음에 발견된 것만 바꾸는것
		#1 : 워드의 모든 문서를 range객체로 만드는 것
		"""
		self.vars["wdReplaceOne"] = 1
		range_obj = self.doc.Range(Start=0, End=self.doc.Characters.Count)  # 1
		range_obj.Find.Execute(search_text, False, False, False, False, False, True, 1, True, replace_text, 1)

	def replace_selection_text_to_input_text(self, replace_text):
		"""
		selection값을 변경
		:param replace_text: 바꿀 문자
		"""
		self.selection.Text = replace_text

	def replace_selection_to_input_text(self, input_value):
		"""
		선택한 영역의 모든문자를 변경하는 것

		:param input_value:
		"""
		self.word_application.Selection.Delete()
		self.word_application.Selection.InsertBefore(input_value)

	def replace_text_for_xy_list(self, input_position_l2d, replace_text):
		"""
		find함수들에서 찾은 위치들을 가지고, 값을 변경하는데
		길이가 다를수가 있기때문에 맨뒤에서부터 바꾸는 것을 해야 한다
		:param input_position_l2d:
		:param replace_text:
		"""
		input_position_l2d.sort()
		input_position_l2d.reverse()
		for l1d in input_position_l2d:
			# print(l1d)
			range_obj = self.doc.Range(Start=l1d[0], End=l1d[1])
			range_obj.Text = replace_text

	def run_font_style(self, input_list):
		self.check_font_style(self, *input_list)
		if self.font_dic["size"]:
			self.selection.Font.Size = self.font_dic["size"]
		if self.font_dic["bold"]:
			self.selection.Font.Bold = self.font_dic["bold"]
		if self.font_dic["italic"]:
			self.selection.Font.Italic = self.font_dic["italic"]
		if self.font_dic["underline"]:
			self.selection.Font.Underline = self.font_dic["underline"]
		if self.font_dic["strikethrough"]:
			self.selection.Font.StrikeThrough = self.font_dic["strikethrough"]
		if self.font_dic["color"]:
			self.selection.Font.TextColor.RGB = self.font_dic["color"]
		if self.font_dic["align"]:
			self.selection.ParagraphFormat.Alignment = self.font_dic["align"]

	def save(self, file_name=""):
		"""
		화일 저장하기

		:param file_name:
		"""
		if file_name == "":
			self.doc.Save()
		else:
			self.doc.SaveAs(file_name)

	def save_as(self, file_name):
		"""
		다른이름으로 화일을 저장

		:param file_name:
		"""
		self.doc.SaveAs(file_name)

	def save_as_pdf(self, file_name):
		"""
		pdf로 저장

		:param file_name:
		"""
		self.doc.SaveAs(file_name, FileFormat=2)

	def search_all_with_color_and_return_position(self, input_text):
		"""
		전체 화일에서 입력글자를 찾아서 색깔을 넣기

		:param input_text:
		:return:
		"""
		result = []
		while self.selection.Find.Execute(input_text):
			self.selection.Range.Font.Italic = True
			self.selection.Range.Font.Color = 255
			self.selection.Range.HighlightColorIndex = 11
			start_no = self.selection.Range.Start
			end_no = start_no + len(input_text)
			temp = [start_no, end_no, self.selection.Range.Text]
			result.append(temp)
		return result

	def select_all(self):
		"""
		전체문서를 선택
		"""
		self.selection.WholeStory()

	def select_bookmark_by_name(self, bookmark_name):
		"""
		북마크의 이름을 기준으로 그 영역을 선택하는 것

		:param bookmark_name:
		"""
		my_range = self.doc.Bookmarks(bookmark_name).Range
		my_range.Select()

	def select_by_xy(self, x, lengh):
		"""
		영역을 선택하는 것
		맨앞에서 몇번째부터，얼마의 길이를 선택할지를 선정

		:param x:
		:param lengh:
		"""
		self.doc.Range(x, x + lengh).Select()

	def select_current_char(self):
		self.move_cursor_to_end_of_selection()

	def select_current_line(self):
		self.select_current_line_form_end_of_selection()

	def select_current_line_form_end_of_selection(self):
		"""
		현재 위치에서 줄의 끝까지 선택
		"""
		self.move_cursor_to_end_of_selection()
		self.get_line_at_cursor()

	def select_current_line_form_start_of_selection(self):
		"""
		현재 위치에서 줄의 끝까지 선택
		"""
		self.move_cursor_to_start_of_selection()
		self.get_line_at_cursor()

	def select_current_para(self):
		self.select_current_para_form_end_of_selection()

	def select_current_para_form_end_of_selection(self):
		"""
		현재 위치의 문단을 선택
		"""
		self.move_cursor_to_end_of_selection()
		self.selection.Expand(self.vars["wdParagraph"])

	def select_current_para_form_start_of_selection(self):
		"""
		현재 위치의 문단을 선택
		"""
		self.move_cursor_to_start_of_selection()
		self.selection.Expand(self.vars["wdParagraph"])

	def select_current_sentence(self):
		self.select_current_sentence_form_end_of_selection()

	def select_current_sentence_form_end_of_selection(self):
		"""
		현재 위치에서 줄의 처음까지
		"""
		self.move_cursor_to_end_of_selection()
		self.selection.Expand(self.vars["wdSentence"])

	def select_current_sentence_form_start_of_selection(self):
		"""
		현재 위치에서 줄의 처음까지
		"""
		self.move_cursor_to_start_of_selection()
		self.selection.Expand(self.vars["wdSentence"])

	def select_current_word(self):
		self.select_current_word_form_end_of_selection()

	def select_current_word_form_end_of_selection(self):
		"""
		현재 위치에서 단어까지 확대 된다
		단, 현재 단어가 중간에서 시작되면 단어의 처음부터 선택되어진다
		"""
		self.move_cursor_to_end_of_selection()
		self.selection.Expand(self.vars["wdWord"])

	def select_current_word_form_start_of_selection(self):
		"""
		현재 위치에서 단어까지 확대 된다
		단, 현재 단어가 중간에서 시작되면 단어의 처음부터 선택되어진다
		"""
		self.move_cursor_to_start_of_selection()
		self.selection.Expand(self.vars["wdWord"])

	def select_doc_by_name(self, input_name):
		"""
		현재 open된 문서중 이름으로 active문서로 활성화 시키기

		:param input_name:
		"""
		self.doc = self.word_application.Documents(input_name)
		self.doc.Activate()

	def select_from_cursor_to_next_para(self, input_no=1):
		self.select_next_nth_letter_type("para", input_no)

	def select_from_cursor_to_next_sentence(self, input_no=1):
		"""
		기준점 : 현재위치

		:param input_no:
		:return:
		"""
		self.select_next_nth_letter_type("sentence", input_no)

	def select_from_cursor_to_next_word(self, input_no=1):
		"""
		기준점 : 현재위치

		char, word는 moveright를 사용해야 한다
		:return:
		"""
		self.select_next_nth_letter_type("word", input_no)

	def select_from_cursor_to_nth_line(self, line_no):
		"""
		(라인 선택) 전체 문서에서 줄수로 선택하는것

		:param line_no: 라인번호
		:return:
		"""
		self.selection.MoveDown(Unit=self.vars["wdLine"], Count=line_no)
		self.selection.Expand(self.vars["wdLine"])

	def select_from_range_to_next_nth_word(self, input_range="", input_no=1):
		"""
		양수 / 음수 => 다가능
		현재 range 의 맨뒷부분에서 n 번째 워드를 선택
		양수일때，range 의 뒷부분으로 curso「가 이동, 뒤로 입력된 숫자만큼 이동한다
		단어 : 공백으로 구분되거나 숫자나 문자의 묶음들、만약 숫주와문자가 섞여있으면，그것으로 구분한다

		:param input_range:
		:param input_no:
		"""
		letter_type_no = self.check_letter_type_no("word")
		step_no = 1
		if input_no < 0:
			input_no = input_no - 1
			step_no = -2
		elif input_no == 0:
			input_no = -1
		if input_range == "":
			input_range = self.get_range_object_for_selection()
		input_range.Move(letter_type_no, input_no)
		start_x = input_range.Start
		input_range.Move(letter_type_no, 1)
		start_y = input_range.Start
		new_range = self.doc.Range(start_x, start_y)
		return new_range

	def select_from_range_to_next_nth_word_by_space(self, input_range="", input_no=1):
		"""
		현재 range 의 맨뒷부분에서 n 번째 워드를 선택
		양수일때，range 의 뒷부분으로 cursor 가 이동, 뒤로 입력된 숫자만큼 이동한다
		단어 : 공백으로 구분되거나 숫자나 문자의 묶음들, 만약 숫주와문자가 섞여있으면, 그것으로 구분한다
		우리가 생각하는 단어 : 맨앞은 글자로 시작하고 맨뒤는 공백이며, 이 공백까지 포함한 사이의 모든 문자들

		:param input_range:
		:param input_no:
		"""
		if input_range == "":
			input_range = self.get_range_object_for_selection()
		total_len = len(self.doc.Characters)
		count_space = 0
		no = input_range.End
		result_text = ""
		while True:
			one_text = self.doc.Range(no, no + 1).Text
			if one_text == " " or one_text == "\r":
				count_space = count_space + 1
			if count_space == input_no:
				result_text = result_text + one_text
			elif count_space == input_no + 1:
				return result_text.strip()
			if total_len < no:
				return result_text.strip()
			no = no + 1
		return end_range

	def select_from_range_to_nth_char(self, input_range="", input_no=1):
		# 현재 위치에서 n번째의 라인
		# "cell": 12, "char": 1, "word": 2, "line": 5, "sentence": 3, "para": 4, "column": 9, "item": 16,  "row": 10, "section": 8, "story": 6, "table": 15,
		if input_range == "":
			input_range = self.get_range_object_for_selection()
		self.selection.MoveRight(Unit=1, Count=input_no - 1)
		self.selection.Expand(1)

	def select_from_range_to_nth_line(self, input_range="", input_no=1):
		# "cell": 12, "char": 1, "word": 2, "line": 5, "sentence": 3, "para": 4, "column": 9, "item": 16,  "row": 10, "section": 8, "story": 6, "table": 15,
		input_range = self.check_range(input_range)
		input_range.MoveDown(Unit=5, Count=input_no, Extend=1)

	def select_from_range_to_nth_para(self, input_range="", input_no=1):
		"""
		현재 range에서 n번째 para 끝까지 선택

		:param input_range:
		:param input_no:
		:return:
		"""
		# "cell": 12, "char": 1, "word": 2, "line": 5, "sentence": 3, "para": 4, "column": 9, "item": 16,  "row": 10, "section": 8, "story": 6, "table": 15,
		input_range = self.check_range(input_range)
		input_range.MoveDown(Unit=4, Count=input_no, Extend=1)

	def select_from_range_to_nth_word(self, input_range="", input_no=1):
		# "cell": 12, "char": 1, "word": 2, "line": 5, "sentence": 3, "para": 4, "column": 9, "item": 16,  "row": 10, "section": 8, "story": 6, "table": 15,
		input_range = self.check_range(input_range)
		input_range.MoveDown(Unit=2, Count=input_no, Extend=1)

	def select_from_range_to_nth_word_1(self, input_range="", input_no=1):
		# "cell": 12, "char": 1, "word": 2, "line": 5, "sentence": 3, "para": 4, "column": 9, "item": 16,  "row": 10, "section": 8, "story": 6, "table": 15,
		if input_range == "":
			input_range = self.get_range_object_for_selection()

		start_x = input_range.Start
		input_range.MoveRight(Unit=2, Count=input_no)
		start_y = input_range.End

		input_range.Start = start_x
		input_range.End = start_y
		return input_range

	def select_from_range_to_previous_nth_word_by_space(self, input_range="", input_no=1):
		"""
		현재 range 의 맨뒷부분에서 n 번째 워드를 선택
		양수일때，range 의 뒷부분으로 cursor 가 이동, 뒤로 입력된 숫자만큼 이동한다
		단어 : 공백으로 구분되거나 숫자나 문자의 묶음들，만약 숫주와문자가 섞여있으면，그것으로 구분한다
		우리가 생각하는 단어 : 맨앞은 글자로 시작하고 맨뒤는 공백이며，이 공백까지 포함한 사이의 모든 문자들

		:param input_range:
		:param input_no:
		"""
		input_no = input_no * -1
		if input_range == "":
			input_range = self.get_range_object_for_selection()
		count_space = 0
		no = input_range.End
		result_text = ""
		while True:
			one_text = self.doc.Range(no, no + 1).Text
			if one_text == " " or one_text == "\r":
				count_space = count_space + 1
			if count_space == input_no:
				# print("==> ", one_text)
				result_text = one_text + result_text
			elif count_space == input_no + 1:
				return result_text.strip()
			if 1 > no:
				return result_text.strip()
			no = no - 1
		return end_range

	def select_from_selection_to_end_of_current_line(self):
		"""
		현재 선택영역에서 라인의 끝까지 선택을 확장

		고쳐야함 : 선택영역에 색을 칠하면 전체 라인이 색칠해 진다
		"""
		self.word_application.Selection.Collapse()
		self.word_application.Selection.EndOf(5, 1)

	def select_from_selection_to_nth_char(self, input_no):
		self.expand_selection_to_nth_char(input_no)

	def select_from_selection_to_nth_letter_type(self, letter_type, input_no):
		"""
		선택영역을 기존 선택영역을 기준으로 이동시키는 것이다
		선택영역의

		movedown이 되는 것
		"cell" = 12, "character" = 1, "char" = 1, "column" = 9
		"item" = 16, "line" = 5, "paragraph" = 4, "para" = 4
		"row" = 10, "section" = 8, "sentence" = 3, "story" = 6
		"table" = 15, "word" = 2


		:param input_no: 라인번호
		"""
		letter_type_no = self.check_letter_type_no(letter_type)
		if input_no > 0:
			if letter_type_no in [3, 2, 1]:
				self.selection.MoveRight(Unit=letter_type_no, Count=input_no, Extend=1) # Extend = 0 은 이동을 시키는 것이다
			else:
				self.selection.MoveDown(Unit=letter_type_no, Count=input_no, Extend=1)
		else:
			if letter_type_no in [3, 2, 1]:
				self.selection.MoveLeft(Unit=letter_type_no, Count=input_no, Extend=1)
			else:
				self.selection.MoveUp(Unit=letter_type_no, Count=input_no, Extend=1)

	def select_from_selection_to_nth_line(self, input_no):
		self.expand_selection_to_nth_line(input_no)

	def select_from_selection_to_nth_para(self, input_no):
		"""
		현재 선택영역에서 n번째 para 끝까지 선택을 확장
		"""
		self.expand_selection_to_nth_para(input_no)

	def select_from_selection_to_nth_word(self, input_no):
		self.expand_selection_to_nth_word(input_no)

	def select_from_selection_to_one_line(self, input_no=1):
		"""
		현재 선택영역에서 라인의 끝까지 선택을 확장
		"""
		self.word_application.Selection.Collapse()
		self.word_application.Selection.MoveDown(Unit=5, Count=input_no, Extend=1)
		#self.word_application.Selection.EndOf(5, 1)
	def select_from_selection_to_previous_nth_char(self, input_no):
		input_no = abs(input_no)
		self.expand_selection_to_nth_char(input_no*-1)

	def select_from_selection_to_previous_nth_line(self, input_no):
		input_no = abs(input_no)
		self.expand_selection_to_nth_line(input_no*-1)

	def select_from_selection_to_previous_nth_para(self, input_no):
		input_no = abs(input_no)
		self.expand_selection_to_nth_para(input_no*-1)

	def select_from_selection_to_previous_nth_word(self, input_no):
		input_no = abs(input_no)
		self.expand_selection_to_nth_word(input_no*-1)

	def select_from_selection_to_start_of_line(self):
		"""
		현재 선택영역에서 라인의 시작점까지 선택, 반대 부분으로 선택하는 것이다
		"""
		self.word_application.Selection.Collapse()
		self.word_application.Selection.StartOf(5, 1)

	def select_from_start_of_doc_to_next_nth_letter_type(self, letter_type, input_no):
		"""
		현재 위치에서 n번째뒤의 단어, 라인들을 선택하는 것
		:return:
		"""
		self.move_cursor_to_start_of_doc()
		checked_letter_type = self.check_letter_type(letter_type)
		#print(checked_letter_type)
		letter_type_no = self.check_letter_type_no(checked_letter_type)
		if input_no > 0:
			if checked_letter_type in ["char", "word", "line"]:
				self.selection.MoveRight(Unit=letter_type_no, Count=input_no-1, Extend=0)
				self.selection.MoveRight(Unit=letter_type_no, Count=1, Extend=1)
			else:
				self.selection.MoveDown(Unit=letter_type_no, Count=input_no-1, Extend=0)
				self.selection.MoveDown(Unit=letter_type_no, Count=1, Extend=1)
		else:
			if checked_letter_type in ["char", "word", "line"]:
				self.selection.MoveLeft(Unit=letter_type_no, Count=input_no-1, Extend=0)
				self.selection.MoveLeft(Unit=letter_type_no, Count=1, Extend=1)
			else:
				self.selection.MoveUp(Unit=letter_type_no, Count=input_no-1, Extend=0)
				self.selection.MoveUp(Unit=letter_type_no, Count=1, Extend=1)

	def select_from_start_of_doc_to_nth_char(self, input_no):
		self.move_cursor_to_start_of_doc()
		self.select_from_selection_to_nth_letter_type("char", input_no)

	def select_from_start_of_doc_to_nth_letter_type(self, letter_type, input_no=1):
		"""
		원하는 순서의 라인의 첫번째 위치로 이동

		:param input_no: 번호
		"""
		letter_type_no = self.check_letter_type_no(letter_type)
		self.selection.GoTo(What=letter_type_no, Which=1, Count=input_no)
		result = self.word_application.Selection.range.Text
		return result

	def select_from_start_of_doc_to_nth_line(self, input_no):
		"""
		기준점 : 문서의 시작
		어디까지 : n번째 라인 끝까지, 문서의 처음부터 n번째 line까지 선택하는 것

		:param input_no: 1번째부터 시작하는 번호
		:return:
		"""
		self.move_cursor_to_start_of_doc()
		self.select_from_selection_to_nth_letter_type("line", input_no-1)

	def select_from_start_of_doc_to_nth_para(self, input_no):
		self.move_cursor_to_start_of_doc()
		self.select_from_selection_to_nth_letter_type("para", input_no-1)

	def select_from_start_of_doc_to_nth_sentence(self, input_no):
		self.move_cursor_to_start_of_doc()
		self.select_from_selection_to_nth_letter_type("sentence", input_no-1)

	def select_from_start_of_doc_to_nth_word(self, input_no):
		self.move_cursor_to_start_of_doc()
		self.select_from_selection_to_nth_letter_type("word", input_no-1)

	def select_line_at_cursor(self):
		"""
		현재 커서가 있는 라인 전체를 선택
		"""
		start_line_no_at_cursor = self.selection.Information(10)
		self.select_from_start_of_doc_to_nth_line(start_line_no_at_cursor)
		self.expand_selection_to_nth_line(1)
		return self.word_application.Selection.Text

	def select_line_at_cursor_v1(self):
		"""
		현재 커서가 있는 라인 전체를 선택
		"""
		self.word_application.Selection.Collapse()
		self.word_application.Selection.Expand(5)

	def select_multi_char_in_line(self, line_no, start_no, count_no):
		"""
		(글자 선택) 전체 문서에서 몇번째 라인의 앞에서 a~b까지의 글자를 선택하는 것

		:param line_no: 줄번호
		:param start_no: 글자의 시작번호
		:param count_no: 글자의 갯수
		"""
		self.selection.GoTo(What=3, Which=line_no, Count=count_no)
		self.selection.Move(Unit=count_no)
		result = self.word_application.Selection.range.Text
		return result

	def select_multi_char_in_para(self, para_no, y, length):
		"""
		(글자 선택) 문단 번호로 문단 전체의 영역을 선택하는 것
		paragraph 를 선택한다, 없으면 맨처음부터

		:param para_no:
		:param y:
		:param length:
		"""
		paragraph = self.doc.Paragraphs(para_no)
		# 맨앞에서 몇번째부터，얼마의 길이를 선택할지를 선정
		x = paragraph.Range.Start + y - 1
		y = paragraph.Range.Start + y + length - 1
		self.vars["ganada"]["new_range"] = self.doc.Range(x, y).Select()

	def select_multi_selection_basic(self, line_no_start=1, line_len=3, letter_type="line"):
		"""
		전체 문서에서 줄수로 선택하는것

		:param line_no_start: 시작번호
		:param line_len:
		:param input_content:
		"""

		letter_type_no = self.check_letter_type_no(letter_type)
		# 현재 selction위치를 저장한다
		x = self.selection.Range.Start
		y = self.selection.Range.End

		# 시작점의 위치를 얻어낸다
		self.selection.MoveDown(Unit=letter_type_no, Count=line_no_start)
		self.selection.Expand(letter_type_no)
		x_start = self.selection.Range.Start

		# 원래위치로 이동한다
		self.doc.Range(x, y).Select()
		# 마지막위치로 이동한다
		self.selection.MoveDown(Unit=letter_type_no, Count=line_no_start + line_len)
		self.selection.Expand(letter_type_no)

		y_end = self.selection.Range.End
		self.doc.Range(x_start, y_end).Select()

	def select_next_basic(self, input_type, input_count=1, expand_type=1):
		"""
		기본적인 형태로 사용이 가능하도록 만든것

		:param input_type:
		:param input_count:
		:param expand_type:
		"""
		checked_input_type = self.check_content_name(input_type)
		type_dic = {"line": 5, "paragraph": 4, "word": 2, "sentence": 3, }
		try:
			self.selection.MoveDown(Unit=type_dic[checked_input_type], Count=input_count)
		except:
			self.selection.MoveRight(Unit=type_dic[checked_input_type], Count=input_count)
		self.selection.Expand(expand_type)

	def select_next_char(self, input_no=1):
		self.select_next_nth_letter_type("char", input_no)

	def select_next_line_from_selection(self, input_no=1):
		self.select_next_nth_letter_type("line", input_no)

	def select_next_nth_letter_type(self, letter_type, input_no):
		"""
		현재 위치에서 n번째뒤의 단어, 라인들을 선택하는 것
		:return:
		"""
		checked_letter_type = self.check_letter_type_no(letter_type)
		letter_type_no = self.check_letter_type_no(checked_letter_type)
		if input_no > 0:
			if checked_letter_type in ["char", "word", "line"]:
				self.selection.MoveRight(Unit=letter_type_no, Count=input_no-1, Extend=0)
				self.selection.MoveRight(Unit=letter_type_no, Count=1, Extend=1)
			else:
				self.selection.MoveDown(Unit=letter_type_no, Count=input_no-1, Extend=0)
				self.selection.MoveDown(Unit=letter_type_no, Count=1, Extend=1)
		else:
			if checked_letter_type in ["char", "word", "line"]:
				self.selection.MoveLeft(Unit=letter_type_no, Count=input_no-1, Extend=0)
				self.selection.MoveLeft(Unit=letter_type_no, Count=1, Extend=1)
			else:
				self.selection.MoveUp(Unit=letter_type_no, Count=input_no-1, Extend=0)
				self.selection.MoveUp(Unit=letter_type_no, Count=1, Extend=1)

	def select_nth_char_from_start_of_doc(self, input_no):
		"""
		문서의 처음을 기준으로 n번째 word를 선택
		:param input_no: 1번째부터 시작하는 번호
		:return:
		"""
		self.move_cursor_to_start_of_doc()
		self.move_cursor_to_nth_char_from_selection(input_no-1)

	def select_nth_line_from_selection(self, input_no):
		self.select_next_nth_letter_type("line", input_no-1)

	def select_nth_line_from_start_of_doc(self, input_no):
		"""
		문서의 처음을 기준으로 n번째 word를 선택
		:param input_no: 1번째부터 시작하는 번호
		:return:
		"""
		self.move_cursor_to_start_of_doc()
		self.move_cursor_to_nth_line_from_selection(input_no-1)
		self.select_current_line()

	def select_nth_para_from_selection(self, input_no):
		self.select_next_nth_letter_type("para", input_no-1)

	def select_nth_para_from_start_of_doc(self, input_no):
		"""
		문서의 처음을 기준으로 n번째 para를 선택하는 것
		:param input_no: 1번째부터 시작하는 번호
		:return:
		"""
		self.move_cursor_to_start_of_doc()
		self.move_cursor_to_nth_para_from_selection(input_no-1)
		self.select_current_para()

	def select_nth_sentence_from_start_of_doc(self, input_no):
		self.move_cursor_to_start_of_doc()
		self.move_cursor_to_nth_sentence_from_selection(input_no-1)
		self.select_current_sentence()

	def select_nth_word_from_selection(self, input_no):
		self.select_next_nth_letter_type("word", input_no-1)

	def select_nth_word_from_start_of_doc(self, input_no):
		self.move_cursor_to_start_of_doc()
		self.move_cursor_to_nth_word_from_selection(input_no-1)
		self.select_current_word()

	def select_previous_basic(self, input_type, input_count=1, expand_type=1):
		"""
		입력형태에 따라서 영역을 선택하는것
		기본적인 형태로 사용이 가능하도록 만든것

		:param input_type:
		:param input_count:
		:param expand_type:
		"""
		checked_input_type = self.check_content_name(input_type)
		type_dic = {"line": 5, "paragraph": 4, "word": 2, "sentence": 3, }
		try:
			self.selection.MoveUp(Unit=type_dic[checked_input_type], Count=input_count)
		except:
			self.selection.MoveLeft(Unit=type_dic[checked_input_type], Count=input_count)
		self.selection.Expand(expand_type)

	def select_range(self):
		"""
		range 객체의 일정부분을 영역으로 선택
		"""
		self.selection = self.doc.Range(0, 0)

	def select_table_by_index(self, table_index):
		"""
		테이블 번호로 테이블을 선택

		:param table_index:
		"""
		self.word_application.Tables(table_index).Select()

	def select_xy_cell_in_table(self, table_index, table_xy_no):
		"""

		:param table_index:
		:param table_xy_no:
		"""
		table = self.doc.Tables(table_index)
		# table_x_no = table.Rows.Count
		table_y_no = table.Columns.Count
		x = table_xy_no[0]
		y = table_xy_no[1]
		mok, namuji = divmod(y, table_y_no)
		if namuji == 0 and mok > 0:
			mok = mok - 1
			namuji = table_y_no
		if mok > 0:
			x = x + mok
			y = namuji
		range = table.Cell(x, y).Range
		range.Select()

	def select_xy_from_start_of_doc(self, start_no, end_no):
		self.selection.Start = start_no
		self.selection.End = end_no
		self.selection.Select()

	def selection_background_color(self):
		"""
		선택영역의 배경색을 빨간색으로 변경
		"""
		self.selection.Font.Shading.BackgroundPatternColor = 255

	def set_active_doc(self):
		"""
		현재 활성화된 문서를 기본 문서로 설정
		"""
		self.doc = self.word_application.ActiveDocument

	def set_bookmark_at_range(self, input_range, bookmark_name):
		"""
		북마크를 영역으로 설정

		:param input_range:
		:param bookmark_name:
		"""
		input_range.Bookmarks.Add(Name=bookmark_name)

	def set_bookmark_by_xy(self, xy, bookmark_name):
		"""
		북마크를 이름으로 설정

		:param xy:
		:param bookmark_name:
		"""
		my_range = self.new_range_by_xy(xy)
		my_range.Bookmarks.Add(Name=bookmark_name)

	def set_default_font(self, *input_list):
		self.font_dic_default = {}
		check_bold = self.vars["check_bold"]
		check_italic = self.vars["check_italic"]
		check_underline = self.vars["check_underline"]
		check_breakthrough = self.vars["check_breakthrough"]
		check_alignment = self.vars["check_alignment"]
		for one in input_list[1:]:
			if one in check_bold.keys():
				self.font_dic_default["bold"] = True
			elif one in check_italic.keys():
				self.font_dic_default["italic"] = True
			elif one in check_underline.keys():
				self.font_dic_default["underline"] = True
			elif one in check_breakthrough.keys():
				self.font_dic_default["strikethrough"] = True
			elif one in check_alignment.keys():
				self.font_dic_default["align"] = self.vars["check_alignment"][one]
			elif type(one) == type(123) and one < 100:
				self.font_dic_default["size"] = one
			elif self.is_scolor_style(one):
				self.font_dic_default["color"] = self.color.change_scolor_to_rgbint(one)
		return self.font_dic_default

	def set_default_font_for_selection(self):
		"""
		기본설정된 font로 적용하는것
		:param reset_selection:
		"""
		self.font_dic["bold"] = False
		self.font_dic["italic"] = False
		self.font_dic["underline"] = False
		self.font_dic["strikethrough"] = False
		self.font_dic["size"] = 11
		self.font_dic["color"] = 197379
		self.font_dic["align"] = 0

		self.selection.Font.Size = self.font_dic["size"]
		self.selection.Font.Bold = self.font_dic["bold"]
		self.selection.Font.Italic = self.font_dic["italic"]
		self.selection.Font.Underline = 0
		self.selection.Font.StrikeThrough = self.font_dic["strikethrough"]
		self.selection.Font.TextColor.RGB = self.font_dic["color"]
		self.selection.ParagraphFormat.Alignment = self.font_dic["align"]

	def set_font_borderline_all_for_selection(self, input_range="", style="", size="", color=""):
		if input_range == "": input_range = self.selection
		for num in [-1, -2, -3, -4]:
			if style != "": input_range.Font.Borders(num).LineStyle = style  # wdLineStyleDouble 7.
			if size != "": input_range.Font.Borders(num).Lineidth = size  # wdLineWidth075pt
			if color != "": input_range.Font.Borders(num).ColorIndex = color  # 7 :yellow

	def set_font_borderline_bottom_for_selection(self, input_range="", style="", size="", color=""):
		if input_range == "": input_range = self.selection
		if style != "": input_range.Font.Borders(-3).LineStyle = style  # wdLineStyleDouble 7
		if size != "": input_range.Font.Borders(-3).LineWidth = size  # wdLineWidth075pt 6
		if color != "": input_range.Font.Borders(-3).ColorIndex = color  # 7 :yellow

	def set_font_borderline_left_for_selection(self, input_range="", style="", size="", color=""):
		if input_range == "": input_range = self.selection
		if style != "": input_range.Font.Borders(-2).LineStyle = style
		if size != "": input_range.Font.Borders(-2).LineWidth = size
		if color != "": input_range.Font.Borders(-2).ColorIndex = color

	def set_font_borderline_right_for_selection(self, input_range="", style="", size="", color=""):
		if input_range == "": input_range = self.selection
		if style != "": input_range.Font.Borders(-4).LineStyle = style
		if size != "": input_range.Font.Borders(-4).LineWidth = size
		if color != "": input_range.Font.Borders(-4).ColorIndex = color

	def set_font_borderline_top_for_selection(self, input_range="", style="", size="", color=""):
		if input_range == "": input_range = self.selection
		if style != "": input_range.Font.Borders(-1).LineStyle = style
		if size != "": input_range.Font.Borders(-1).LineWidth = size
		if color != "": input_range.Font.Borders(-1).ColorIndex = color

	def set_font_color_in_selection(self, scolor):
		rgbint = self.color.change_scolor_to_rgbint(scolor)
		self.selection.Font.Color = rgbint

	def set_font_in_range_with_setup(self, range_object="", input_list=[]):
		"""
		3. 영역에 적용한다
		"""
		if range_object == "":
			range_object = self.selection

		self.setup_font_default()  # 기본으로 만든다
		if input_list:
			# 아무것도 없으면, 기존의 값을 사용하고, 있으면 새로이 만든다
			if type(input_list) == type([]):
				self.setup_font(input_list)
			elif type(input_list) == type({}):
				# 만약 사전 형식이면, 기존에 저장된 자료로 생각하고 update한다
				self.vars["font"].update(input_list)

		range_object.Font.Size = self.vars["font"]["size"]
		range_object.Font.Bold = self.vars["font"]["bold"]
		range_object.Font.Italic = self.vars["font"]["italic"]
		range_object.Font.Name = self.vars["font"]["name"]

		range_object.Font.Strikethrough = self.vars["font"]["strikethrough"]
		range_object.Font.Subscript = self.vars["font"]["subscript"]
		range_object.Font.Superscript = self.vars["font"]["superscript"]
		range_object.Font.Underline = self.vars["font"]["underline"]
		rgbint = self.color.change_scolor_to_rgbint(self.vars["font"]["color"])
		range_object.Font.Color = rgbint

	def set_font_name_for_table(self, input_no="Georgia"):
		"""
		테이블의 폰트이름을 설정

		:param input_no:
		"""
		self.word_application.table(input_no).Font.Name = input_no

	def set_font_name_for_xy_cell_in_table(self, table_index, cell_index, input_no="Georgia"):
		"""
		테이블의 xy의 폰트를 설정

		:param table_index:
		:param cell_index:
		:param input_no:
		"""
		table = self.word_application.Tables(table_index)
		table(cell_index).Font.Name = input_no

	def set_font_options_for_reuse(self, *input_list):
		self.check_font_style(self, input_list)

	def set_font_options_for_selection(self, input_list):
		self.run_font_style(input_list)

	def set_font_size_down_for_selection(self):
		"""
		선택한것의 폰트를 한단계 내리기
		"""
		self.selection.Font.Shrink()

	def set_font_size_for_table(self, table_index, font_size=10):
		"""
		표에 대한 글자크기를 설정

		:param table_index:
		:param font_size:
		"""
		table = self.doc.Tables(table_index)
		table.Font.Size = font_size

	def set_font_size_up_for_range(self, input_range_object=""):
		"""
		선택한것의 폰트를 한단계 올린다
		"""
		range_obj = self.check_range_object(input_range_object)
		range_obj.Font.Grow()

	def set_font_style_for_selection(self, input_range="", color=""):
		"""
		######## 변경 필요
		선택한 영역에 언더라인을 적용
		"""
		if input_range == "": input_range = self.selection
		input_range.Font.UnderlineColor = color
		self.selection.Font.StrikeThrough = True

		self.selection.Font.Underline = 1  # wdUnderlineSingle = 1, A single line

	def set_footer(self):
		"""
		헤더를 삽입
		"""
		for section in self.doc.Sections:
			# header를 하나씩 설정할수는 없다
			section.Headers(1).PageNumbers.Add(PageNumberAlignment=2, FirstPage=True)
			section.Headers(1).PageNumbers.ShowFirstPageNumber = True
			section.Headers(1).PageNumbers.RestartNumberingAtSection = True
			section.Headers(1).PageNumbers.StartingNumber = 1

	def set_header(self):
		"""
		헤더를 삽입
		"""
		for section in self.doc.Sections:
			# header를 하나씩 설정할수는 없다
			section.Headers(1).PageNumbers.Add(PageNumberAlignment=2, FirstPage=True)
			section.Headers(1).PageNumbers.ShowFirstPageNumber = True
			section.Headers(1).PageNumbers.RestartNumberingAtSection = True
			section.Headers(1).PageNumbers.StartingNumber = 1

	def set_header_new(self):
		"""
		헤더를 삽입
		"""
		page_no = 0
		for section in self.doc.Sections:
			section.Headers(1).Range.Fields.Update()
			headersCollection = section.Headers
			for header in headersCollection:
				header.Range.Fields.Update()
				page_no = page_no + 111
				# print("헤더", page_no)
				aaa = header.Range
				aaa.Select()
				header.Range.Text = "헤더 : " + str(page_no)
				# aaa.Font.Bold = True
				# aaa.ParagraphFormat.Alignment = 1
				new_table = self.doc.Tables.Add(Range=aaa, NumRows=1, NumColumns=3, DefaultTableBehavior=0,
												AutoFitBehavior=0)
				new_table.Cell(1, 3).range.ParagraphFormat.Alignment = 0
				new_table.Cell(1, 3).range.Text = "헤더 : " + str(page_no)

		for section in self.doc.Sections:
			HeaderTablesCount = section.Headers(1).Range.Tables.Count
			FooterTablesCount = section.Footers(1).Range.Tables.Count

			for index in range(HeaderTablesCount):
				HeaderTable = section.Headers(1).Range.Tables(index + 1)
				HeaderTable.Cell(1, 1).Range.Text = index

	def set_height_for_table_obj(self, table_obj, i_height=10):
		# table_obj.Rows.SetHeight(RowHeight := InchesToPoints(0.5), HeightRule := wdRowHeightExactly)
		table_obj.Rows.Height = i_height

	def set_line_width_for_table(self, table_obj, inside_width="", outside_width=""):
		"""
		테이블의 선두께

		:param table_obj:  테이블 객제
		:param inside_width:
		:param outside_width:
		"""
		table_obj.Borders.InsideLineWidth = self.vars["ganada"]["line_width"][inside_width]
		table_obj.Borders.OutsideLineWidth = self.vars["ganada"]["line_width"][outside_width]

	def set_margin_of_bottom(self, input_value=20):
		"""
		페이지의 아래 마진을 설정

		:param input_value:
		"""
		self.doc.PageSetup.BottomMargin = input_value

	def set_margin_of_left_for_page(self, input_value=20):
		"""
		페이지셋업 : 왼쪽 띄우기

		:param input_value:
		"""
		self.doc.PageSetup.LeftMargin = input_value

	def set_margin_of_top_for_page(self, input_value=20):
		"""
		페이지셋업 : 위쪽 띄우기

		:param input_value:
		"""
		self.doc.PageSetup.TopMargin = input_value

	def set_orientation_for_page(self, input_value=20):
		"""
		페이지의 회전을 설정

		:param input_value:
		"""
		self.doc.PageSetup.Orientation = input_value

	def set_page_no_at_header(self, left_text="", right_start_no=1):
		"""

		:param left_text:
		:param right_start_no:
		"""
		self.doc.Sections(1).Headers(1).Range.Text = left_text
		self.doc.Sections(1).Headers(1).PageNumbers.StartingNumber = right_start_no
		self.doc.Sections(1).Headers(1).PageNumbers.Add(True)

	def set_range_by_xy(self, x, y):
		my_range = self.doc.Range(x, y)
		return my_range

	def set_range_from_start_of_doc_to_char(self, input_no):
		new_range = self.select_from_start_of_doc_to_nth_letter_type("char", input_no)
		return new_range

	def set_range_from_start_of_doc_to_nth_char(self, input_no=1):
		self.set_range_from_start_of_doc_to_nth_letter_type("char", input_no)

	def set_range_from_start_of_doc_to_nth_letter_type(self, letter_type, input_no=1):
		"""
		movedown이 되는 것
		"cell" = 12, "character" = 1, "char" = 1, "column" = 9
		"item" = 16, "line" = 5, "paragraph" = 4, "para" = 4
		"row" = 10, "section" = 8, "sentence" = 3, "story" = 6
		"table" = 15, "word" = 2
		"""
		letter_type_no = self.check_letter_type_no(letter_type)
		my_range = self.doc.Range(0, 0)
		my_range.MoveDown(Unit=letter_type_no, Count=input_no - 1)
		my_range.Expand(letter_type_no)

	def set_range_from_start_of_doc_to_nth_line(self, input_no):
		new_range = self.select_from_start_of_doc_to_nth_letter_type("line", input_no)
		return new_range

	def set_range_from_start_of_doc_to_nth_para(self, input_no):
		new_range = self.select_from_start_of_doc_to_nth_letter_type("para", input_no)
		return new_range

	def set_range_from_start_of_doc_to_nth_word(self, input_no):
		new_range = self.select_from_start_of_doc_to_nth_letter_type("word", input_no)
		return new_range

	def set_range_object_from_letter_nol_to_letter_no2(self, start_no, end_no):
		my_range = self.doc.Range(start_no > end_no)
		return my_range

	def set_range_object_from_x_to_y(self, start_no, end_no):
		"""
		영역 선택

		:param start_no:
		:param end_no:
		"""
		my_range = self.doc.Range(start_no, end_no)
		return my_range

	def set_right_margin_for_page(self, input_value=20):
		"""
		페이지셋업 : 오른쪽 띄우기
		:param input_value:
		"""
		self.doc.PageSetup.RightMargin = input_value

	def set_space_size_for_selection(self, input_range="", input_value=1.5):
		if input_range == "": input_range = self.selection
		input_range.Font.Spacing = input_value

	def set_start_range_from_selection_start(self, letter_type, input_no=1):
		"""
		선택영역의 첫커서부분을 range객체의 시작점으로 만드는 것
		"""
		a = self.selection.Start
		my_range = self.doc.Range(a, a)
		self.expand_range_to_nth_letter_type(my_range, letter_type, input_no)

	def set_style_for_selection(self, style_name="표준"):
		"""
		선택한 영역의 글씨 스타일을 변경한다

		:param style_name:
		"""
		self.selection.Style = self.doc.Styles(style_name)

	def setup_font(self, input_list):
		"""
		기존적인 폰트의 설정
		["진하게", 12, "red50", "밑줄"] 이런형식으로 들어오면 알아서 값이 되는 것이다
		"""
		if self.vars["font"]:
			# 하위값이 있으면, 기존의것을 사용하고, 아무것도 없으면 기본값으로 설정한다
			pass
		else:
			self.setup_font_default()

		for one in input_list:
			if type(one) == type(123):
				self.vars["font"]["size"] = one
			elif one in ["진하게", "굵게", "찐하게", "bold"]:
				self.vars["font"]["bold"] = True
			elif one in ["italic", "이태리", "이태리체", "기울기"]:
				self.vars["font"]["italic"] = True
			elif one in ["strikethrough", "취소선", "통과선", "strike"]:
				self.vars["font"]["strikethrough"] = True
			elif one in ["subscript", "하위첨자", "밑첨자"]:
				self.vars["font"]["subscript"] = True
			elif one in ["superscript", "위첨자", "웃첨자"]:
				self.vars["font"]["superscript"] = True
			elif one in ["underline", "밑줄"]:
				self.vars["font"]["underline"] = True
			elif one in ["vertical", "수직", "가운데"]:
				self.vars["font"]["align_v"] = 3
			elif one in ["horizental", "수평", "중간"]:
				self.vars["font"]["align_h"] = 2
			elif one in self.color.vars["check_color_name"].keys():
				self.vars["font"]["color"] = one
			else:
				self.vars["font"]["name"] = one

		result = copy.deepcopy(self.vars["font"])
		return result

	def setup_font_default(self):
		"""
		1. 기본자료를 만든다
		"""
		# 기본값을 만들고, 다음에 이것을 실행하면 다시 기본값으로 돌아온다

		self.vars["font"]["bold"] = False
		self.vars["font"]["color"] = "bla"
		self.vars["font"]["italic"] = False
		self.vars["font"]["name"] = "Arial"
		self.vars["font"]["size"] = 12
		self.vars["font"]["strikethrough"] = False
		self.vars["font"]["subscript"] = False
		self.vars["font"]["superscript"] = False
		self.vars["font"]["alpha"] = False  # tintandshade를 이해하기 쉽게 사용하는 목적
		self.vars["font"]["underline"] = False
		self.vars["font"]["align_v"] = 3  # middle =3, top = 1, bottom = 4, default=2
		self.vars["font"]["align_h"] = 1  # None =1, center=2, left=1, default=1
		self.vars["font"]["color"] = 1

	def split_all_doc_by_style_name_as_list_2d(self):
		"""
		전체 문서를 스타일이 다른것을 기준으로 분리하는 것
		"""
		result = []
		story_all = []

		start = ""
		style_name = ""
		title = ""
		for para in self.doc.Paragraphs:
			story_or_title = para.Range.Text
			style = para.Style.NameLocal

			if style == "표준":
				story_all.append(story_or_title)
			else:
				if start == "":
					if story_all == []:
						story_all = [[]]
					result.append(["무제", "제목", story_all])
					story_all = []
					start = "no"
					style_name = style
					title = story_or_title
				else:
					result.append([title, style_name, story_all])
					style_name = style
					title = story_or_title
					start = "no"
					story_all = []

		return result

	def terms(self):
		result = """
		no :  1부터 시작하는 번호
		index : 0부터시작하는 번호
		object : 객체를 뜻하는 것

		ComputeStatistics : 워드에서 특정 텍스트나 문서 전체에 대한 다양한 정보를 얻을 수 있는 기능

		"""
		return result

	def unmerge_for_table(self, table_object, start_x, start_y):
		"""
		워드는 unmerge가 없으며, 셀분할로 만들어야 한다

		:param table_object:  테이블 객제
		:param start_x:
		:param start_y:
		"""
		count_y = table_object.Columns.Count
		count_x = table_object.Rows.Count

	def write_list_2d_with_new_table(self, input_list_2d):
		# 2차원 자료를 알아서 테이블만들어서 넣기
		x_len = len(input_list_2d)
		y_len = len(input_list_2d[0])
		table_object = self.new_table_with_black_line(x_len, y_len)
		for x in range(1, x_len + 1):
			for y in range(1, y_len + 1):
				table_object.Cell(Row=x, Column=y).Range.Text = input_list_2d[x - 1][y - 1]

	def write_list_2d_with_style(self, input_list_2d):
		"""
		[['050630\r', '제목', '\\n\x0c']] ==> [제목, 제목의 스타일이름, 내용]
		위와같은 형태의 자료를 새로운 워드를 오픈해서 작성하는것

		:param input_list_2d:
		"""
		total_len = len(input_list_2d)
		for index, list_1d in enumerate(input_list_2d):
			# print("완료된 %는 ==> ", index / total_len * 100)
			title = str(list_1d[0]).strip()
			style_name = str(list_1d[1])
			text_data_old = list_1d[2]
			text_data = ""

			for index, one in enumerate(text_data_old):
				text_data = text_data + one

			# 스타일이 있는 제목 부분을 나타내는 코드
			cursor = self.doc.Characters.Count  # 워드의 가장 뒷쪽으로 커서위치를 설정
			self.selection.Start = cursor
			self.selection.End = cursor + len(title)
			self.selection.InsertAfter(title)
			self.selection.Style = self.doc.Styles(style_name)  # 스타일 지정하는 코드

			# 스타일이 없는 부분을 표준으로 설정해서 나타내는 코드
			self.selection.InsertAfter("\r\n")
			cursor = self.doc.Characters.Count  # 커서의 현재위치 확인
			self.selection.Start = cursor
			self.selection.InsertAfter(text_data)
			self.selection.End = cursor + len(text_data)
			self.selection.Style = self.doc.Styles("표준")  # 스타일 지정하는 코드
			self.selection.InsertAfter("\r\n")

	def write_text(self, input_text):
		self.write_text_for_end_of_selection(input_text)

	def write_text_as_list_1d_for_each_para(self):
		"""
		모든 paragraph를 리스트로 만들어서 돌려주는 것
		"""
		result = []
		para_nums = self.doc.Paragraphs.Count
		for no in range(1, para_nums + 1):
			result.append(self.doc.Paragraphs(no).Range.Text)
		return result

	def write_text_at_begin_of_cursor(self, input_value):
		self.write_text_at_start_of_cursor(input_value)

	def write_text_at_end_of_cursor(self, input_value):
		"""
		선택한것의 뒤에 글씨넣기

		:param input_value:
		:return:
		"""
		self.selection.InsertAfter(input_value)

	def write_text_at_end_of_doc(self, input_text):
		"""
		문서의 제일 뒷부분에 글을 넣는것
		"""
		self.doc.Content.InsertAfter(input_text)

	def write_text_at_end_of_nth_para(self, para_no=1, input_text="hfs1234234234;lmk"):
		"""
		문단의 번호로 선택된 문단의 제일 뒷부분에 글을 넣는것

		:param para_no:
		:param input_text:
		"""
		self.doc.Paragraphs(para_no - 1).Content.InsertAfter(input_text)

	def write_text_at_end_of_selection(self, input_text):
		"""
		선택한 영역의 제일 뒷부분에 text값을 값을 넣것
		:param input_text: 입력값
		"""
		self.word_application.Selection.EndOf()
		self.selection.InsertBefore(input_text)

	def write_text_at_nth_cell_in_table(self, table_index, input_no=1, input_text=""):
		"""
		테이블의 n번째 셀에 값넣기

		:param table_index:
		:param input_no:
		:param input_text:
		:return:
		"""

		table = self.doc.Tables(table_index)
		y_line = table.Columns.Count
		#print(y_line)
		mok, namuji = divmod(input_no, y_line)
		table.Cell(mok+1, namuji).Range.Text = str(input_text)

	def write_text_at_start_of_cursor(self, input_value):
		"""
		문제가 되었던 부분은, self.selection은 워드프로그램에서 1개만 설정이 되는것이라,
		각각을 활성화를 하지 않 은면，2개 이상의 워드프로그램에서는 문제가 발생할 간으성이 높으므로，
		selection을 사용하는 함수에서는 위와 같은 부분을 넣어주어야 문제가 생기지 않는다

		:param input_value:
		"""
		self.doc.Activate()
		self.selection.InsertBefore(input_value)
		self.doc.Activate()

	def write_text_at_start_of_doc(self, input_text):
		"""
		문서의 제일 앞부분에 글을 넣는것

		:param input_text:
		"""
		self.move_cursor_to_start_of_doc()
		self.write_text_at_start_of_selection(input_text)

	def write_text_at_start_of_selection(self, input_text):
		"""
		선택한 영역의 제일 앞부분에 text값을 값을 넣것

		:param input_text: 입력값
		"""
		self.selection.InsertBefore(input_text)

	def write_text_at_xy_cell_in_table(self, input_table_no, xy, input_text):
		"""
		테이블의 셀 위치에 값넣기

		:param input_table_no:
		:param xy:
		:param input_text:
		:return:
		"""
		self.doc.Tables(input_table_no).Cell(int(xy[0]), int(xy[1])).Range.Text = str(input_text)

	def write_text_for_end_of_selection(self, input_text="aaaaaaaa"):
		"""
		선택한 영역의 제일 뒷부분에 text값을 값을 넣것

		:param input_text: 입력값
		"""
		self.move_cursor_to_end_of_selection()
		self.write_text_at_start_of_selection(input_text)

	def write_text_for_selection_with_color_size_bold(self, i_text, i_color="red", i_size=11, i_bold=False):
		"""

		:param i_text:
		:param i_color:
		:param i_size:
		:param i_bold:
		"""
		# 현재 선택된 영역에 글씨를 넣는것
		my_range = self.word_application.Selection.Range
		my_range.Text = i_text
		my_range.Bold = i_bold
		my_range.Font.Size = i_size
		my_range.Font.Color = self.color.change_scolor_to_rgbint(i_color)
		my_range.Select()

	def write_text_for_selection_with_font_style(self, input_value, *option_font_list):
		"""
		선택영역의 맨 뒷부분에 폰트형식으로 글씨쓰기

		:param input_value:
		"""
		self.move_cursor_to_end_of_selection()
		char_sno = self.selection.End
		self.selection.InsertAfter(input_value)
		self.select_xy_from_start_of_doc(char_sno, char_sno + len(input_value))

		if option_font_list:
			self.set_default_font_for_selection()
			self.run_font_style(option_font_list)
			self.move_cursor_to_end_of_selection()

	def write_text_in_selection_with_color_size_bold(self, i_text, i_color="red", i_size=11, i_bold=False):
		"""

		:param i_text:
		:param i_color:
		:param i_size:
		:param i_bold:
		:return:
		"""
		# 현재 선택된 영역에 글씨를 넣는것
		my_range = self.word_application.Selection.Range
		my_range.Text = i_text
		my_range.Bold = i_bold
		my_range.Font.Size = i_size
		my_range.Font.Color = self.vars["ganada"]["color_24bit"][i_color]
		my_range.Select()

	def write_text_in_table_by_xy(self, table_object="", xy="", input_text=""):
		"""
		테이블의 셀에 글씨 입력하기

		:param table_index:
		:param xy:
		:param input_text:
		"""
		table_object = self.check_table_object(table_object)
		table_object.Cell(int(xy[0]), int(xy[1])).Range.Text = str(input_text)

	def write_text_in_table_to_nth_cell(self, table_index, input_no=1, input_text=""):
		"""
		테이블의 맨 첫번째셀이 1번인것 부터 오른쪽으로 n번째 셀에 값넣기
		"""

		table_object = self.check_table_object(table_index)
		y_line = table_object.Columns.Count
		mok, namuji = divmod(input_no, y_line)
		table_object.Cell(mok + 1, namuji).Range.Text = str(input_text)

	def write_text_with_new_line_at_end_of_doc(self, input_text):
		"""
		문서의 맨 뒷부분에 글을쓰고 다음줄로 만드는 것
		"""
		self.doc.Content.InsertAfter(input_text + "\r\n")

	def write_text_with_style_at_end_of_doc(self, input_text, style_name):
		"""
		문서의 맨 뒷부분에 글을쓰고 스타일을 적용하는 것

		:param input_text:
		:param style_name:
		"""
		self.move_cursor_to_end_of_selection()
		self.doc.Content.InsertAfter(input_text + "\r\n")
		self.selection.Start = self.selection.Range.Start
		self.selection.End = self.selection.Start + len(input_text)
		self.selection.Style = self.doc.Styles(style_name)  # 스타일 지정하는 코드

	def insert_check_box_at_selection(self):
		#현재 위치에 체크박스를 넣는것
		#3:콤보박스
		self.doc.ContentControls.Add(8, self.selection)

	def paint_scolor_for_yline_in_table(self, table_obj, y_no, scolor="red"):
		#테이블객체의 가로세로번호의 설의 배경색을 색칠하기
		rgb_int = self.color.change_scolor_to_rgbint(scolor)
		table_obj.Columns(y_no).Shading.BackgroundPatternColor = rgb_int