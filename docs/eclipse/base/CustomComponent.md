# 绘制自定义组件

## SWT 绘图基础

Eclipse RCP 使用 SWT (Standard Widget Toolkit) 来构建用户界面。SWT 提供了强大的自定义绘图能力，允许开发者创建完全自定义的组件。

### SWT 绘图核心类

- **GC (Graphics Context)**: 图形上下文，提供所有绘图操作
- **Canvas**: 空白画布控件，可以在上面自由绘制
- **PaintListener**: 绘制事件监听器
- **Image**: 图像对象，可以在内存中绘制
- **Color**: 颜色对象
- **Font**: 字体对象

## 基本自定义组件

### 创建简单的自定义组件

```java
package com.example.widgets;

import org.eclipse.swt.SWT;
import org.eclipse.swt.events.PaintEvent;
import org.eclipse.swt.events.PaintListener;
import org.eclipse.swt.graphics.GC;
import org.eclipse.swt.graphics.Rectangle;
import org.eclipse.swt.widgets.Canvas;
import org.eclipse.swt.widgets.Composite;

public class SimpleCustomWidget extends Canvas {
    
    private String text = "Custom Widget";
    
    public SimpleCustomWidget(Composite parent, int style) {
        super(parent, style);
        
        // 添加绘制监听器
        addPaintListener(new PaintListener() {
            @Override
            public void paintControl(PaintEvent e) {
                drawWidget(e.gc);
            }
        });
    }
    
    /**
     * 绘制组件
     */
    private void drawWidget(GC gc) {
        Rectangle bounds = getBounds();
        
        // 设置背景色
        gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_WHITE));
        gc.fillRectangle(0, 0, bounds.width, bounds.height);
        
        // 绘制边框
        gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_BLACK));
        gc.drawRectangle(0, 0, bounds.width - 1, bounds.height - 1);
        
        // 绘制文本
        gc.drawText(text, 10, 10, true);
    }
    
    public void setText(String text) {
        this.text = text;
        redraw();  // 触发重绘
    }
    
    public String getText() {
        return text;
    }
}
```

### 使用自定义组件

```java
public class CustomWidgetView extends ViewPart {
    
    @Override
    public void createPartControl(Composite parent) {
        SimpleCustomWidget widget = new SimpleCustomWidget(parent, SWT.NONE);
        widget.setText("Hello Custom Widget!");
    }
    
    @Override
    public void setFocus() {
        // 设置焦点
    }
}
```

## GC 常用绘图方法

### 1. 绘制基本图形

```java
public class BasicShapesWidget extends Canvas {
    
    public BasicShapesWidget(Composite parent, int style) {
        super(parent, style);
        
        addPaintListener(e -> {
            GC gc = e.gc;
            
            // 绘制线条
            gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_RED));
            gc.drawLine(10, 10, 100, 10);
            
            // 绘制矩形
            gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_BLUE));
            gc.drawRectangle(10, 30, 90, 50);
            
            // 填充矩形
            gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_GREEN));
            gc.fillRectangle(120, 30, 90, 50);
            
            // 绘制圆角矩形
            gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_BLACK));
            gc.drawRoundRectangle(10, 100, 90, 50, 10, 10);
            
            // 绘制椭圆
            gc.drawOval(120, 100, 90, 50);
            
            // 填充椭圆
            gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_YELLOW));
            gc.fillOval(230, 100, 90, 50);
            
            // 绘制圆弧
            gc.drawArc(10, 170, 90, 50, 0, 90);
            
            // 绘制多边形
            int[] points = {120, 170, 150, 220, 180, 170, 165, 195};
            gc.drawPolygon(points);
            
            // 填充多边形
            gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_CYAN));
            gc.fillPolygon(points);
        });
    }
}
```

### 2. 绘制文本

```java
public class TextDrawingWidget extends Canvas {
    
    public TextDrawingWidget(Composite parent, int style) {
        super(parent, style);
        
        addPaintListener(e -> {
            GC gc = e.gc;
            
            // 设置字体
            Font font = new Font(getDisplay(), "Arial", 12, SWT.BOLD);
            gc.setFont(font);
            
            // 绘制文本
            gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_BLACK));
            gc.drawText("Hello World!", 10, 10, true);
            
            // 绘制带背景的文本
            gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_YELLOW));
            gc.drawText("Text with Background", 10, 40, false);
            
            // 获取文本尺寸
            String text = "Measured Text";
            org.eclipse.swt.graphics.Point extent = gc.textExtent(text);
            gc.drawText(text, 10, 70);
            gc.drawRectangle(10, 70, extent.x, extent.y);
            
            // 垂直文本（需要变换）
            gc.setTransform(createRotationTransform(getDisplay(), 90));
            gc.drawText("Vertical Text", 10, -150);
            gc.setTransform(null);
            
            // 清理资源
            font.dispose();
        });
    }
    
    private Transform createRotationTransform(Display display, float angle) {
        Transform transform = new Transform(display);
        transform.rotate(angle);
        return transform;
    }
}
```

### 3. 绘制图像

```java
public class ImageDrawingWidget extends Canvas {
    
    private Image image;
    
    public ImageDrawingWidget(Composite parent, int style) {
        super(parent, style);
        
        // 加载图像
        image = new Image(getDisplay(), "icons/sample.png");
        
        addPaintListener(e -> {
            GC gc = e.gc;
            
            // 直接绘制图像
            gc.drawImage(image, 10, 10);
            
            // 缩放绘制图像
            Rectangle bounds = image.getBounds();
            gc.drawImage(image, 
                0, 0, bounds.width, bounds.height,  // 源区域
                150, 10, 100, 100);                  // 目标区域
            
            // 使用透明度绘制
            gc.setAlpha(128);  // 50% 透明
            gc.drawImage(image, 10, 150);
            gc.setAlpha(255);  // 恢复不透明
        });
        
        // 添加释放资源的监听器
        addDisposeListener(e -> {
            if (image != null && !image.isDisposed()) {
                image.dispose();
            }
        });
    }
}
```

## 高级绘图技巧

### 1. 双缓冲绘制

避免闪烁，提高绘制性能。

```java
public class DoubleBufferedWidget extends Canvas {
    
    private Image backBuffer;
    
    public DoubleBufferedWidget(Composite parent, int style) {
        super(parent, style | SWT.DOUBLE_BUFFERED);
        
        addPaintListener(e -> {
            Rectangle bounds = getBounds();
            
            // 创建或重建后备缓冲
            if (backBuffer == null || backBuffer.isDisposed() ||
                !backBuffer.getBounds().equals(new Rectangle(0, 0, bounds.width, bounds.height))) {
                
                if (backBuffer != null && !backBuffer.isDisposed()) {
                    backBuffer.dispose();
                }
                backBuffer = new Image(getDisplay(), bounds.width, bounds.height);
            }
            
            // 在后备缓冲上绘制
            GC bufferGC = new GC(backBuffer);
            try {
                drawContent(bufferGC, bounds.width, bounds.height);
            } finally {
                bufferGC.dispose();
            }
            
            // 将后备缓冲复制到画布
            e.gc.drawImage(backBuffer, 0, 0);
        });
        
        addDisposeListener(e -> {
            if (backBuffer != null && !backBuffer.isDisposed()) {
                backBuffer.dispose();
            }
        });
    }
    
    private void drawContent(GC gc, int width, int height) {
        // 绘制背景
        gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_WHITE));
        gc.fillRectangle(0, 0, width, height);
        
        // 绘制内容
        gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_BLUE));
        for (int i = 0; i < 10; i++) {
            gc.drawOval(i * 20, i * 20, 100, 100);
        }
    }
}
```

### 2. 使用变换

```java
public class TransformWidget extends Canvas {
    
    public TransformWidget(Composite parent, int style) {
        super(parent, style);
        
        addPaintListener(e -> {
            GC gc = e.gc;
            Transform transform = new Transform(getDisplay());
            
            try {
                // 平移
                transform.translate(50, 50);
                gc.setTransform(transform);
                gc.drawRectangle(0, 0, 50, 50);
                
                // 重置变换
                transform.identity();
                
                // 旋转
                transform.translate(150, 75);
                transform.rotate(45);
                gc.setTransform(transform);
                gc.drawRectangle(-25, -25, 50, 50);
                
                // 重置变换
                transform.identity();
                
                // 缩放
                transform.translate(250, 50);
                transform.scale(1.5f, 1.5f);
                gc.setTransform(transform);
                gc.drawRectangle(0, 0, 50, 50);
                
            } finally {
                transform.dispose();
                gc.setTransform(null);
            }
        });
    }
}
```

### 3. 渐变填充

```java
public class GradientWidget extends Canvas {
    
    public GradientWidget(Composite parent, int style) {
        super(parent, style);
        
        addPaintListener(e -> {
            GC gc = e.gc;
            Rectangle bounds = getBounds();
            
            // 线性渐变（垂直）
            gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_BLUE));
            gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_WHITE));
            gc.fillGradientRectangle(10, 10, 100, 100, true);
            
            // 线性渐变（水平）
            gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_RED));
            gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_YELLOW));
            gc.fillGradientRectangle(130, 10, 100, 100, false);
            
            // 使用 Path 创建复杂形状的渐变
            Path path = new Path(getDisplay());
            path.addArc(250, 10, 100, 100, 0, 360);
            
            gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_GREEN));
            gc.fillPath(path);
            
            path.dispose();
        });
    }
}
```

### 4. 抗锯齿

```java
public class AntiAliasWidget extends Canvas {
    
    public AntiAliasWidget(Composite parent, int style) {
        super(parent, style);
        
        addPaintListener(e -> {
            GC gc = e.gc;
            
            // 不使用抗锯齿
            gc.setAntialias(SWT.OFF);
            gc.setLineWidth(3);
            gc.drawOval(10, 10, 100, 100);
            gc.drawText("No Anti-alias", 30, 120);
            
            // 使用抗锯齿
            gc.setAntialias(SWT.ON);
            gc.setLineWidth(3);
            gc.drawOval(150, 10, 100, 100);
            gc.drawText("With Anti-alias", 160, 120);
            
            // 文本抗锯齿
            gc.setTextAntialias(SWT.ON);
            Font font = new Font(getDisplay(), "Arial", 20, SWT.BOLD);
            gc.setFont(font);
            gc.drawText("Smooth Text", 10, 150, true);
            font.dispose();
        });
    }
}
```

## 交互式自定义组件

### 带鼠标交互的组件

```java
public class InteractiveWidget extends Canvas {
    
    private List<Rectangle> rectangles = new ArrayList<>();
    private Rectangle selectedRect = null;
    
    public InteractiveWidget(Composite parent, int style) {
        super(parent, style);
        
        // 初始化矩形
        for (int i = 0; i < 5; i++) {
            rectangles.add(new Rectangle(i * 60 + 10, 10, 50, 50));
        }
        
        // 绘制
        addPaintListener(e -> {
            GC gc = e.gc;
            
            for (Rectangle rect : rectangles) {
                if (rect.equals(selectedRect)) {
                    gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_RED));
                } else {
                    gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_BLUE));
                }
                gc.fillRectangle(rect);
                
                gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_BLACK));
                gc.drawRectangle(rect);
            }
        });
        
        // 鼠标点击事件
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseDown(MouseEvent e) {
                selectedRect = null;
                
                for (Rectangle rect : rectangles) {
                    if (rect.contains(e.x, e.y)) {
                        selectedRect = rect;
                        break;
                    }
                }
                
                redraw();
            }
        });
        
        // 鼠标移动事件（悬停效果）
        addMouseMoveListener(e -> {
            boolean needRedraw = false;
            
            for (Rectangle rect : rectangles) {
                if (rect.contains(e.x, e.y)) {
                    setCursor(getDisplay().getSystemCursor(SWT.CURSOR_HAND));
                    needRedraw = true;
                    break;
                } else {
                    setCursor(null);
                }
            }
            
            if (needRedraw) {
                redraw();
            }
        });
    }
}
```

### 可拖动的组件

```java
public class DraggableWidget extends Canvas {
    
    private Rectangle shape = new Rectangle(50, 50, 100, 100);
    private Point dragStart = null;
    private Rectangle dragStartBounds = null;
    
    public DraggableWidget(Composite parent, int style) {
        super(parent, style);
        
        addPaintListener(e -> {
            GC gc = e.gc;
            
            // 绘制背景
            gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_WHITE));
            Rectangle bounds = getBounds();
            gc.fillRectangle(0, 0, bounds.width, bounds.height);
            
            // 绘制可拖动的形状
            gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_BLUE));
            gc.fillRectangle(shape);
            
            gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_BLACK));
            gc.drawRectangle(shape);
        });
        
        // 鼠标按下
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseDown(MouseEvent e) {
                if (shape.contains(e.x, e.y)) {
                    dragStart = new Point(e.x, e.y);
                    dragStartBounds = new Rectangle(
                        shape.x, shape.y, shape.width, shape.height
                    );
                    setCursor(getDisplay().getSystemCursor(SWT.CURSOR_SIZEALL));
                }
            }
            
            @Override
            public void mouseUp(MouseEvent e) {
                dragStart = null;
                dragStartBounds = null;
                setCursor(null);
            }
        });
        
        // 鼠标拖动
        addMouseMoveListener(e -> {
            if (dragStart != null && dragStartBounds != null) {
                int dx = e.x - dragStart.x;
                int dy = e.y - dragStart.y;
                
                shape.x = dragStartBounds.x + dx;
                shape.y = dragStartBounds.y + dy;
                
                redraw();
            } else if (shape.contains(e.x, e.y)) {
                setCursor(getDisplay().getSystemCursor(SWT.CURSOR_HAND));
            } else {
                setCursor(null);
            }
        });
    }
}
```

## 自定义图表组件

### 简单的柱状图

```java
public class BarChartWidget extends Canvas {
    
    private Map<String, Integer> data = new LinkedHashMap<>();
    
    public BarChartWidget(Composite parent, int style) {
        super(parent, style);
        
        addPaintListener(e -> {
            drawChart(e.gc);
        });
    }
    
    public void setData(Map<String, Integer> data) {
        this.data = data;
        redraw();
    }
    
    private void drawChart(GC gc) {
        Rectangle bounds = getBounds();
        
        // 绘制背景
        gc.setBackground(getDisplay().getSystemColor(SWT.COLOR_WHITE));
        gc.fillRectangle(0, 0, bounds.width, bounds.height);
        
        if (data.isEmpty()) {
            gc.drawText("No Data", bounds.width / 2 - 20, bounds.height / 2);
            return;
        }
        
        // 计算最大值
        int maxValue = data.values().stream()
            .max(Integer::compareTo)
            .orElse(1);
        
        // 图表边距
        int margin = 40;
        int chartWidth = bounds.width - 2 * margin;
        int chartHeight = bounds.height - 2 * margin;
        
        // 绘制坐标轴
        gc.setForeground(getDisplay().getSystemColor(SWT.COLOR_BLACK));
        gc.drawLine(margin, margin, margin, bounds.height - margin);  // Y轴
        gc.drawLine(margin, bounds.height - margin, 
                   bounds.width - margin, bounds.height - margin);     // X轴
        
        // 绘制柱状图
        int barWidth = chartWidth / data.size() - 10;
        int x = margin + 5;
        
        Color barColor = new Color(getDisplay(), 66, 133, 244);
        gc.setBackground(barColor);
        
        for (Map.Entry<String, Integer> entry : data.entrySet()) {
            String label = entry.getKey();
            int value = entry.getValue();
            
            // 计算柱子高度
            int barHeight = (int) ((double) value / maxValue * chartHeight);
            int barY = bounds.height - margin - barHeight;
            
            // 绘制柱子
            gc.fillRectangle(x, barY, barWidth, barHeight);
            gc.drawRectangle(x, barY, barWidth, barHeight);
            
            // 绘制标签
            gc.drawText(label, x, bounds.height - margin + 5, true);
            
            // 绘制数值
            gc.drawText(String.valueOf(value), x, barY - 20, true);
            
            x += barWidth + 10;
        }
        
        barColor.dispose();
    }
}

// 使用示例
public void createChart(Composite parent) {
    BarChartWidget chart = new BarChartWidget(parent, SWT.NONE);
    
    Map<String, Integer> data = new LinkedHashMap<>();
    data.put("Jan", 120);
    data.put("Feb", 150);
    data.put("Mar", 180);
    data.put("Apr", 160);
    data.put("May", 200);
    
    chart.setData(data);
}
```

## 性能优化技巧

### 1. 局部重绘

只重绘需要更新的区域，而不是整个控件。

```java
public void updateRegion(int x, int y, int width, int height) {
    // 只重绘指定区域
    redraw(x, y, width, height, false);
}
```

### 2. 缓存图像

对于复杂的静态内容，可以预先绘制到图像中。

```java
private Image cachedImage;

private Image getCachedImage() {
    if (cachedImage == null || cachedImage.isDisposed()) {
        Rectangle bounds = getBounds();
        cachedImage = new Image(getDisplay(), bounds.width, bounds.height);
        
        GC gc = new GC(cachedImage);
        drawComplexContent(gc);
        gc.dispose();
    }
    return cachedImage;
}
```

### 3. 避免频繁创建资源

```java
// 不好的做法
addPaintListener(e -> {
    Font font = new Font(getDisplay(), "Arial", 12, SWT.NORMAL);
    e.gc.setFont(font);
    e.gc.drawText("Text", 10, 10);
    font.dispose();  // 每次绘制都创建和销毁
});

// 好的做法
private Font font;

public MyWidget(Composite parent, int style) {
    super(parent, style);
    font = new Font(getDisplay(), "Arial", 12, SWT.NORMAL);
    
    addPaintListener(e -> {
        e.gc.setFont(font);
        e.gc.drawText("Text", 10, 10);
    });
    
    addDisposeListener(e -> {
        if (font != null && !font.isDisposed()) {
            font.dispose();
        }
    });
}
```

## 最佳实践

1. **资源管理**: 始终释放创建的 Color、Font、Image 等资源
2. **事件处理**: 避免在绘制事件中执行耗时操作
3. **双缓冲**: 对于复杂或动画组件使用双缓冲减少闪烁
4. **抗锯齿**: 根据需要启用抗锯齿提高视觉效果
5. **局部更新**: 使用 redraw(x, y, width, height) 只更新需要的区域
6. **坐标系统**: 理解 SWT 的坐标系统（左上角为原点）
7. **可访问性**: 考虑高 DPI 显示器的缩放问题
8. **测试**: 在不同操作系统和分辨率下测试自定义组件

## 总结

SWT 提供了强大而灵活的自定义绘图能力，通过组合使用：
- Canvas 作为绘图画布
- GC 提供的各种绘图方法
- PaintListener 响应绘制事件
- 各种鼠标和键盘事件处理

可以创建出功能丰富、性能优良的自定义组件，满足各种复杂的 UI 需求。
