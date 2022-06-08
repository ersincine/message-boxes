from boxes import MessageBox, HorizontalBoxes, VerticalBoxes
from colorama import Fore, Back, Style


if __name__ == "__main__":

    box1 = MessageBox("Cras at lacinia dui, sit amet ultrices elit. Cras tristique, elit eu lacinia dictum, magna dui dignissim lorem, eu dignissim sapien lacus non "
    "sapien. Aliquam dictum malesuada erat, et ultricies risus pulvinar non. Duis ultrices vitae diam nec sagittis. Suspendisse molestie lacus sed faucibus ultrices." 
    "Aenean non dolor a mi maximus elementum. Vivamus non ex ut arcu cursus sagittis et in augue. Aliquam ultricies libero eu orci scelerisque consequat. Etiam" 
    "convallis eget augue sit amet tincidunt. Phasellus eleifend diam quis mollis lobortis. Etiam imperdiet, est ut consectetur suscipit, lorem justo tempus elit," 
    "sit amet pharetra velit leo ac ex. Nunc sapien urna, interdum vel velit at, blandit tempor mi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam "
    "sed eros in lorem semper dignissim venenatis dapibus massa. Etiam rutrum ornare tortor, eget eleifend ligula. Nunc facilisis ante tempus mollis malesuada.",
    title="Warning", width=60, border_color=Fore.RED, text_color=Fore.BLUE)

    box2 = MessageBox("Just a small box", border_color=Fore.GREEN, width=1)
    
    box3 = MessageBox("box", border_color=Fore.YELLOW, width=1)

    box4 = MessageBox("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent lorem quam, malesuada eu quam non, luctus tincidunt purus. Nullam ac erat"
    " quis dui luctus varius eget eu eros. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Praesent erat sapien, consequat"
    " non lorem at, lobortis mollis ex. Nunc sed tortor sed neque imperdiet suscipit at ac ligula. Donec id tortor eget sapien mollis suscipit ac eget ex. Nulla"
    " consectetur, est eget vehicula cursus, purus velit aliquam felis, vitae dignissim diam justo sed dui. Nam mollis sapien id libero aliquet sodales.", 
    width=30, border_color=Fore.WHITE)

    # box1.print()
    # box2.print()

    # boxes = HorizontalBoxes(box1, box2)
    # boxes.print()

    boxes = HorizontalBoxes(box1, VerticalBoxes(box2, box2, box3, align="center"), box4, align="top")
    boxes.print()
