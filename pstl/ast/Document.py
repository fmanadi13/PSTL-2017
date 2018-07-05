from pstl.ast.Node import Node
from pstl.ast.Lists import AQ_Item
from pstl.ast.Headline import *
from pstl.ast.Comment import *
from pstl.ast.Directive import *
from pstl.ast.EmptyLine import *
from pstl.ast.Tabular import AQ_Tabular
from pstl.ast.Figure import AQ_Figure
from pstl.ast.Paragraph import AQ_Paragraph


from pylatex import Document, Figure, Tabular, \
    Itemize, Enumerate, LineBreak, simple_page_number, TikZ, \
    TikZNode, TikZDraw, TikZCoordinate, TikZUserPath, TikZOptions, \
    Package, Tabularx, Center, VerticalSpace, LargeText, TextBlock, FBox
    
from pylatex.utils import NoEscape, bold, italic, escape_latex
from pylatex.base_classes  import ContainerCommand, Arguments, Command
from pstl.ast.pylatex_extend.headfoot import PageStyle, Head, Foot
from pstl.ast.pylatex_extend.parbox import ParBox
from pstl.ast.pylatex_extend.questions import Questions

class AQ_Document(Node):
    """Represents a generic exam file 
    """
    __latex_begin_qcm_env = False
    __latex_qcm_env_object = None

    def __init__(self, ctx, title = ""):
        
        self.document = None
        self.directives = []
        self.filename = "AutoQCM"
        super(AQ_Document, self).__init__(ctx)
        

    
    def setupDocumentPreamble(self):
        r"""Set document properties, variables, extra packages and user defined commands """
        geometry_options = {            
            "width":'170mm',
            "left":"20mm",
            "top":"30mm",
            "bottom":"20mm",
            "head":"20mm"
        }
        
        dclass = "exam"
        dclass_options = ['french', 'a4paper','answers', 'addpoints', '12pt']
        self.document = Document(self.filename, documentclass= dclass, 
                            document_options= dclass_options, 
                            geometry_options=geometry_options)
        self.document.set_variable('class', 'Master d\'informatique')
        self.document.set_variable('examunit', 'ARES')
        self.document.set_variable('allowdocuments', 'Notes de cours autorisées')
        self.document.set_variable('examnum', 'Première Session')
        self.document.set_variable('term', 'Janvier 2014')
        self.document.set_variable('examyear', '2017-2018')
        self.document.set_variable('timelimit', '2 Heures')
        self.document.set_variable('university', 'Université Pièrre et Marie Curie')
        self.document.set_variable('examtitle', 'Examen du 15 décembre 2017')
        self.document.packages.append(Package('qrcode'))
        self.document.packages.append(Package('amssymb'))
        self.document.packages.append(Package('etoolbox'))
        
        self.document.preamble.append(Command('usetikzlibrary', NoEscape('positioning')))
        self.document.preamble.append(Command('checkboxchar', NoEscape('$\Box$')))
        self.document.preamble.append(Command('checkedchar', NoEscape('$\\blacksquare$')))
        self.document.preamble.append(Command('AtBeginEnvironment', arguments=Arguments('checkboxes', NoEscape(r'\par\medskip\begin{minipage}{\linewidth}'))))
        self.document.preamble.append(Command('makeatletter'))
        self.document.preamble.append(Command('AtEndEnvironment', arguments=Arguments('checkboxes', NoEscape(r'\if@correctchoice \endgroup \fi\end{minipage}'))))
        self.document.preamble.append(Command('makeatother'))
  
    def setupDocumentHeader(self):
        """ Set the document header and footer"""
        if not isinstance(self.document, Document):
            return None
        # Add document header
        header = PageStyle("headandfoot")
        self.document.append(Command('headrule'))
        pic1 = TikZ(options=TikZOptions({'node distance':'5mm'}))
        pic2 = TikZ(options=TikZOptions({'node distance':'5mm'}))
        pic3 = TikZ(options=TikZOptions({'node distance':'5mm'}))
        pic4 = TikZ(options=TikZOptions({'node distance':'5mm'}))
        # options for our node
        circle_node_kwargs = {
            'minimum size': '0.5cm',
            'fill': 'black'
            }

        # create our test node
        left_circle = TikZNode(
                        handle='lCircle',
                        options=TikZOptions('draw',
                                           'circle',
                                           anchor= 'west',
                                           **circle_node_kwargs))
        right_circle = TikZNode(
                        handle='rCircle',
                        options=TikZOptions('draw',
                                           'circle',
                                           anchor= 'east',
                                           **circle_node_kwargs))
        qr_node = TikZNode(
                        handle = 'QR',
                        text=NoEscape("\qrcode[version=5, height=1.5cm]{fares}"),
                        options = TikZOptions(
                            left='of rCircle')
                        )
        box_node_kwargs ={
            'minimum height':'1.5cm',
            'minimum width':'4cm',
            }
        student_number_label = TikZNode(
                        text= 'Numéro d étudiant',
                        handle= 'SNL',
                        options = TikZOptions(
                            right='of lCircle')
                        )


        student_number_box = TikZDraw([TikZCoordinate(-1.25, -1),
                             TikZUserPath('grid'),
                             TikZCoordinate(1.25, 0.75)],
                              options=TikZOptions(
                                  step='0.25cm', border='gray', thikness = 'very thick'))
        #student_number_box = TikZNode(
        #                text= '',
        #                handle= 'SNB',
        #                options = TikZOptions(
        #                    'draw',
        #                    right='of SNL',
        #                    step = '.25cm',
        #                    border = 'gray',
        #                    thikness = 'thick',
        #                    **box_node_kwargs)
        #                )
        # add to tikzpicture
        pic1.append(left_circle)
        pic1.append(student_number_label)
        pic1.append(student_number_box)
        pic2.append(right_circle)
        pic2.append(qr_node)
        pic3.append(left_circle)
        pic4.append(right_circle)
        # Create left header
        with self.document.create(Head("L")):
            self.document.append(pic1)
        # Create center header
        #with header.create(Head("C")):
            #header.append(simple_page_number())
        # Create right header
        with self.document.create(Head("R")):
            self.document.append(pic2)
        # Create left footer
        with self.document.create(Foot("L")):
            self.document.append(pic3)
        # Create center footer
        with self.document.create(Foot("C")):
            self.document.append("Center Footer")
        # Create right footer
        with self.document.create(Foot("R")):
            self.document.append(pic4)

        #header.change_thickness('header', 0.5)
        self.document.preamble.append(header)
        self.document.append(Command('noindent'))
        with self.document.create(Tabularx(table_spec ='c X c',width_argument=NoEscape('\linewidth'))) as tab:
            tab.append(Command('centering'))
            tab.add_row([bold(NoEscape(Command('class').dumps_as_content())), 
                         bold(NoEscape("Module "+ Command('examunit').dumps_as_content())), 
                         bold(NoEscape(Command('university').dumps_as_content()))
                         ])
            tab.add_row([italic(NoEscape(Command('allowdocuments').dumps_as_content())), 
                         italic(NoEscape("Durée " + Command('timelimit').dumps_as_content())), 
                         italic(NoEscape("Année " + Command('examyear').dumps_as_content()))
                         ])

        with self.document.create(Center()) as c:
            c.append(VerticalSpace('1em'))
            c.append(bold(NoEscape(LargeText(NoEscape(Command('examtitle').dumps_as_content())).dumps_as_content())))
            c.append(VerticalSpace('1em'))

        notice_box = FBox()
        notice_parbox = ParBox(width = NoEscape('0.95\\textwidth'))
        
        notice_parbox.append(bold('Important'))
        notice_parbox.append(LineBreak())
        notice_parbox.append(NoEscape(r'Cet examen contient \numpages\ pages (cette page incluse) et \numquestions\ questions.Total of points is \numpoints\
                             Rest of introduction. Rest of introduction. Rest of introduction. Rest of introduction. Rest of introduction. Rest of introduction. Rest of introduction. Rest of introduction.'))
        notice_box.append(notice_parbox)
        with self.document.create(Center()) as c:
            c.append(Command('setlength'))
            c.append(Command('fboxrule', '1pt'))
            c.append(Command('setlength'))
            c.append(Command('fboxsep', '1em'))
            c.append(notice_box)


    def _initDirectives(self):
        r"""Filter the ast directives to get only those refering to document """
        __local_directive_names = ["caption", "name", "attr_latex"]
        __doc_directives = list(filter(
            lambda x: 
                isinstance(x, AQ_Directive) and x.getName().lower() not in __local_directive_names, 
                self.children))
        
        
        return __doc_directives

    def _initLocalDirectives(self):
        __local_directive_names = ["caption", "name", "attr_latex"]
        _caption = ""
        _name = ""
        _attr_latex = ""
        __local_directive_names = ["caption", "name", "attr_latex"]
        for child in self.children:
            if isinstance(child, AQ_Directive) and child.getName().lower() in __local_directive_names:
                if child.getName().lower() == 'caption':
                    _caption = child.value
                elif child.getName().lower() == 'name':
                    _name = child.value
                elif child.getName().lower() == 'attr_latex':
                    _attr_latex = child.value
            elif isinstance(child, AQ_Tabular):
                if _caption != "" or _name != "" or _attr_latex != "":
                    child.caption = _caption
                    child.name = _name
                    child.attr_latex = _attr_latex
            elif isinstance(child, AQ_Paragraph):
                if _caption != "" or _name != "" or _attr_latex != "":
                    for line in child.children:
                        for span in line.children:
                            if isinstance(span, AQ_Figure):
                                span.caption = _caption
                                span.name = _name
                                span.attr_latex = _attr_latex
                                break




    def getDirectiveByName(self, name):
        """Get document directive by its name"""
        if name == None or name =="":
            return None
        else:
            for d in self.directives:
                if d.getName() == name:
                    return d
            return None


    def latex(self):
        r"""Convert the ast document object into latex document object, so we
            can export it later to a pdf file."""
        self.setupDocumentPreamble()
        self.setupDocumentHeader()
        self.directives = self._initDirectives()
        self._initLocalDirectives()

        for child in self.children:
            if isinstance(child, AQ_Directive):
                continue
            if isinstance(child, AQ_Headline):
                # First question, so we start our questions environment
                if(AQ_Document.__latex_begin_qcm_env == False and child.isQuestion):
                    AQ_Document.__latex_begin_qcm_env = True
                    AQ_Document.__latex_qcm_env_object = Questions()

            if(AQ_Document.__latex_begin_qcm_env == True):
                AQ_Document.__latex_qcm_env_object.append(child.latex())

        self.document.append(AQ_Document.__latex_qcm_env_object)
        return self.document

    def __repr__(self):
        return f"{self.location}\n<document>\n"+ ('\n'.join([c.__repr__() for c in self.children])) +"\n</document>"

    def __str__(self):
        return f"{self.location}\n<document>\n"+ ('\n'.join([c.__repr__() for c in self.children])) +"\n</document>"
